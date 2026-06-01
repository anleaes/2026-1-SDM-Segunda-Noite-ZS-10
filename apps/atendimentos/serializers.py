from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Atendimento, DoseAtendimento


class AtendimentoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)
    unidade_saude_nome = serializers.CharField(source='unidade_saude.nome', read_only=True)
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True, allow_null=True)

    class Meta:
        model = Atendimento
        fields = [
            'id', 'paciente', 'paciente_nome',
            'unidade_saude', 'unidade_saude_nome',
            'profissional', 'profissional_nome',
            'data_atendimento', 'status', 'observacao'
        ]

    def validate(self, attrs):
        inst = self.instance
        status_ = attrs.get('status', getattr(inst, 'status', None))
        data = attrs.get('data_atendimento', getattr(inst, 'data_atendimento', None))
        if status_ == 'realizado' and data and data > timezone.now():
            raise serializers.ValidationError(
                {'data_atendimento': 'Um atendimento realizado não pode ter data no futuro.'}
            )
        return attrs


def _ordem_para_int(valor):
    """Converte a ordem da dose (CharField) para inteiro, validando."""
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise serializers.ValidationError(
            {'ordem_dose': 'A ordem da dose deve ser um número inteiro.'}
        )


class DoseAtendimentoSerializer(serializers.ModelSerializer):
    vacina_nome = serializers.CharField(source='vacina.nome', read_only=True)
    lote_numero = serializers.CharField(source='lote.numero_lote', read_only=True)

    class Meta:
        model = DoseAtendimento
        fields = [
            'id', 'atendimento',
            'vacina', 'vacina_nome',
            'lote', 'lote_numero',
            'ordem_dose', 'observacao'
        ]

    def validate(self, attrs):
        inst = self.instance
        atendimento = attrs.get('atendimento') or getattr(inst, 'atendimento', None)
        vacina = attrs.get('vacina') or getattr(inst, 'vacina', None)
        lote = attrs.get('lote') or getattr(inst, 'lote', None)
        ordem_raw = attrs.get('ordem_dose', getattr(inst, 'ordem_dose', None))
        ordem = _ordem_para_int(ordem_raw)

        # 1. O lote precisa pertencer à vacina escolhida.
        if lote and vacina and lote.vacina_id != vacina.id:
            raise serializers.ValidationError(
                {'lote': 'O lote selecionado não pertence à vacina informada.'}
            )

        # 2. A dose só pode ser registrada em atendimento realizado.
        if atendimento and atendimento.status != 'realizado':
            raise serializers.ValidationError(
                {'atendimento': 'A dose só pode ser registrada em um atendimento com status "realizado".'}
            )

        # 3. A ordem precisa estar dentro do esquema da vacina.
        if vacina and (ordem < 1 or ordem > vacina.quantidade_doses):
            raise serializers.ValidationError(
                {'ordem_dose': f'A ordem deve estar entre 1 e {vacina.quantidade_doses} (total de doses desta vacina).'}
            )

        # 4. Lote dentro da validade e com estoque (só exige se o lote mudou).
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

        # 5/6. Regras que dependem do histórico do paciente nesta vacina.
        if atendimento and vacina:
            irmas = DoseAtendimento.objects.filter(
                vacina=vacina, atendimento__paciente_id=atendimento.paciente_id
            ).select_related('atendimento')
            if inst:
                irmas = irmas.exclude(pk=inst.pk)

            anterior_data = None
            for d in irmas:
                try:
                    o = int(d.ordem_dose)
                except (TypeError, ValueError):
                    continue
                # 5. Não pode repetir a mesma ordem para o mesmo paciente.
                if o == ordem:
                    raise serializers.ValidationError(
                        {'ordem_dose': f'O paciente já recebeu a {ordem}ª dose desta vacina.'}
                    )
                # Guarda a data da maior dose anterior, para o intervalo.
                if o < ordem and d.atendimento and d.atendimento.data_atendimento:
                    if anterior_data is None or d.atendimento.data_atendimento > anterior_data:
                        anterior_data = d.atendimento.data_atendimento

            # 6. Respeitar o intervalo mínimo entre doses.
            if (
                vacina.intervalo_dias and ordem > 1 and anterior_data
                and atendimento.data_atendimento
            ):
                minimo = anterior_data + timedelta(days=vacina.intervalo_dias)
                if atendimento.data_atendimento < minimo:
                    raise serializers.ValidationError(
                        {'ordem_dose': f'É necessário aguardar {vacina.intervalo_dias} dias desde a dose anterior.'}
                    )

        return attrs
