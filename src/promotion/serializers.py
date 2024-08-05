from rest_framework import serializers


from . import models


class PromotionConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PromotionCondition
        fields = '__all__'
        extra_kwargs = {
            'group': {'write_only': True, 'required': False},
        }


class PromotionConditionGroupSerializer(serializers.ModelSerializer):
    conditions = PromotionConditionSerializer(many=True, required=False)
    
    class Meta:
        model = models.PromotionConditionGroup
        fields = '__all__'
        extra_kwargs = {
            'promotion': {'write_only': True, 'required': False},
        }


class PromotionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PromotionResult
        fields = '__all__'
        extra_kwargs = {
            'promotion': {'write_only': True, 'required': False},
        }


class PromotionSerializer(serializers.ModelSerializer):
    condition_groups = PromotionConditionGroupSerializer(many=True, required=False)
    results = PromotionResultSerializer(many=True, required=False)
    
    class Meta:
        model = models.Promotion
        fields = '__all__'


class PromotionCreateUpdateSerializer(serializers.ModelSerializer):
    condition_groups = PromotionConditionGroupSerializer(many=True, required=False)
    results = PromotionResultSerializer(many=True, required=False)
    
    class Meta:
        model = models.Promotion
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'condition_groups': {'required': False},
            'results': {'required': False},
        }
    
    def create(self, validated_data):
        condition_groups_data = validated_data.pop('condition_groups')
        results_data = validated_data.pop('results')
        
        promotion = models.Promotion.objects.create(**validated_data)
    
        for group_data in condition_groups_data:
            conditions_data = group_data.pop('conditions')
            group = models.PromotionConditionGroup.objects.create(promotion=promotion, **group_data)
            for condition_data in conditions_data:
                cond = models.PromotionCondition.objects.create(group=group, **condition_data)
        
        for result_data in results_data:
            models.PromotionResult.objects.create(promotion=promotion, **result_data)
        
        return promotion

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
        instance.save()

        if 'condition_groups' in validated_data:
            condition_groups_data = validated_data.pop('condition_groups')
            instance.condition_groups.all().delete()
            for group_data in condition_groups_data:
                if 'conditions' not in group_data:
                    continue
                conditions_data = group_data.pop('conditions')
                group = models.PromotionConditionGroup.objects.create(promotion=instance, **group_data)
                for condition_data in conditions_data:
                    models.PromotionCondition.objects.create(group=group, **condition_data)

        if 'results' in validated_data:
            results_data = validated_data.pop('results')
            instance.results.all().delete()
            for result_data in results_data:
                models.PromotionResult.objects.create(promotion=instance, **result_data)

        return instance
