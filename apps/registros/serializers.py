from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import RegistroVacinacao


def _dose_para_int(valor):
    """Converte o campo 'dose' (CharField) para inteiro, validando."""
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise serializers.ValidationError(
            {'dose': 'A dose deve ser um número inteiro.'}
        )


class RegistroVacinacaoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)
    vacina_nome = serializers.CharField(source='vacina.nome', read_only=True)
    lote_numero = serializers.CharField(source='lote.numero_lote', read_only=True)
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True, allow_null=True)
    unidade_saude_nome = serializers.CharField(source='unidade_saude.nome', read_only=True)

    class Meta:
        model = RegistroVacinacao
        fields = [
            'id', 'paciente', 'paciente_nome',
            'vacina', 'vacina_nome',
            'lote', 'lote_numero',
            'profissional', 'profissional_nome',
            'unidade_saude', 'unidade_saude_nome',
            'atendimento',
            'data_aplicacao', 'dose', 'observacao'
        ]

    def validate(self, attrs):
        inst = self.instance
        paciente = attrs.get('paciente') or getattr(inst, 'paciente', None)
        vacina = attrs.get('vacina') or getattr(inst, 'vacina', None)
        lote = attrs.get('lote') or getattr(inst, 'lote', None)
        atendimento = attrs.get('atendimento') or getattr(inst, 'atendimento', None)
        data_aplicacao = attrs.get('data_aplicacao', getattr(inst, 'data_aplicacao', None))
        dose_raw = attrs.get('dose', getattr(inst, 'dose', None))
        dose = _dose_para_int(dose_raw)

        # 1. O lote precisa pertencer à vacina escolhida.
        if lote and vacina and lote.vacina_id != vacina.id:
            raise serializers.ValidationError(
                {'lote': 'O lote selecionado não pertence à vacina informada.'}
            )

        # 2. Só registra aplicação em atendimento realizado.
        if atendimento and atendimento.status != 'realizado':
            raise serializers.ValidationError(
                {'atendimento': 'O registro só pode ser feito em um atendimento com status "realizado".'}
            )

        # 3. A dose precisa estar dentro do esquema da vacina.
        if vacina and (dose < 1 or dose > vacina.quantidade_doses):
            raise serializers.ValidationError(
                {'dose': f'A dose deve estar entre 1 e {vacina.quantidade_doses} (total de doses desta vacina).'}
            )

        # 4. Data de aplicação não pode ser no futuro.
        if data_aplicacao and data_aplicacao > timezone.now().date():
            raise serializers.ValidationError(
                {'data_aplicacao': 'A data da aplicação não pode ser no futuro.'}
            )

        # 5. Lote dentro da validade e com estoque (só exige se o lote mudou).
        if lote:
            lote_alterado = inst is None or inst.lote_id != lote.id
            if lote_alterado:
                hoje = timezone.now().date()
                if lote.data_validade < hoje:
                    raise serializers.ValidationError({'lote': 'O lote selecionado está vencido.'})
                if lote.quantidade_disponivel <= 0:
                    raise serializers.ValidationError(
                        {'lote': 'O lote selecionado não possui doses disponíveis em estoque.'}
                    )

        # 6/7. Regras que dependem do histórico do paciente nesta vacina.
        if paciente and vacina:
            irmaos = RegistroVacinacao.objects.filter(paciente=paciente, vacina=vacina)
            if inst:
                irmaos = irmaos.exclude(pk=inst.pk)

            data_anterior = None
            for r in irmaos:
                try:
                    d = int(r.dose)
                except (TypeError, ValueError):
                    continue
                # 6. Não pode repetir a mesma dose para o mesmo paciente.
                if d == dose:
                    raise serializers.ValidationError(
                        {'dose': f'O paciente já possui registro da {dose}ª dose desta vacina.'}
                    )
                if d < dose and r.data_aplicacao:
                    if data_anterior is None or r.data_aplicacao > data_anterior:
                        data_anterior = r.data_aplicacao

            # 7. Respeitar o intervalo mínimo entre doses.
            if vacina.intervalo_dias and dose > 1 and data_anterior and data_aplicacao:
                minimo = data_anterior + timedelta(days=vacina.intervalo_dias)
                if data_aplicacao < minimo:
                    raise serializers.ValidationError(
                        {'dose': f'É necessário aguardar {vacina.intervalo_dias} dias desde a dose anterior.'}
                    )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        registro = super().create(validated_data)
        lote = registro.lote
        if lote.quantidade_disponivel > 0:
            lote.quantidade_disponivel -= 1
            lote.save(update_fields=['quantidade_disponivel'])
        return registro
