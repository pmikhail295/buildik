import json
from django.db.models import ForeignKey
from typing import Any, Dict, List
import pccomponents.models as pcc
import pccomponents.config as conf
import setups.config as setup_conf


class PCComponentsAPI:
    ItemType = Dict[str, Any]

    def get_object_fields(obj) -> ItemType:
        fields = {}
        for field in type(obj)._meta.fields:
            fields[field.name] = getattr(obj, field.name)
            if isinstance(field, ForeignKey):
                fields[field.name] = getattr(fields[field.name], 'id')

        return fields

    def get_model_fieldnames(model) -> List[str]:
        return [field.name for field in model._meta.fields]

    def get_item(pk: int) -> ItemType:
        try:
            item = pcc.Item.objects.get(id=pk)
        except:
            raise ValueError(f'no item with id {pk}')
        model = pcc.item_class_by_number(item.category)
        return model.objects.get(id=pk).to_json()

    def get_all_items() -> List[ItemType]:
        items = []
        for category in pcc.ITEMS:
            items += [item.to_json() for item in category[2].objects.all()]
        items.sort(key=lambda x:x['id'])
        return items
    
    def get_items(category: str) -> List[ItemType]:
        model = pcc.item_class_by_category(category)
        return [item.to_json() for item in model.objects.all()]

    def filter_translate_from_query(filter_params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            for field_name, spec in pcc.SPECIFICATIONS.items():
                if field_name in filter_params:
                    filter_params[field_name] = spec.objects.get(**{field_name+'_name':filter_params[field_name]})
            
            for model in pcc.REFERENCES:
                for t in pcc.REFERENCES[model]:
                    for field_name in [t[3], "required_"+t[3]]:
                        if field_name in filter_params:
                            queryset = t[0].objects.filter(
                                **{t[0]._meta.model_name+'_name__in': filter_params[field_name]}
                            )
                            if t[2] is None:
                                filter_params[field_name] = list(queryset)
                            else:
                                spec_params = {}
                                for spec in queryset:
                                    spec_params[spec] = filter_params[field_name][getattr(spec, t[0]._meta.model_name+'_name')]
                                filter_params[field_name] = spec_params
            return filter_params
        except:
            raise ValueError("filter cannot be processed, check its correctness")

    def get_items_filtered(category: str, filter_params: Dict[str, Any], error_check:bool=True) -> List[ItemType]:
        model = pcc.item_class_by_category(category)
        model_fields = PCComponentsAPI.get_model_fieldnames(model)


        queryset = model.objects.all()
        filters = {}
        errors = {}
        filter_config = [
            (conf.GREATER_OR_EQUAL_RELATIONS, '__gte'), (conf.LESS_OR_EQUAL_RELATIONS, '__lte'),
            (conf.BELONGING_TO_RELATIONS, '__in'), (conf.NUMBERED_BELONGING_TO_RELATIONS, '__in'),
        ]

        if category+"_number" in filter_params:
            if setup_conf.ITEMS_INFO[model][0] is False and filter_params[category+'_number']:
                queryset = model.objects.none()


        for kfield in conf.EQUAL_RELATIONS:
            if kfield in filter_params:
                if kfield in model_fields:
                    filters[kfield] = filter_params[kfield]
                else:
                    errors[kfield] = f'{category} has no field {kfield}'
                filter_params.pop(kfield)
            
        for filter_case in filter_config:
            for kfield, vfield in filter_case[0].items():
                if vfield in filter_params:
                    if kfield in model_fields:
                        filters[kfield+filter_case[1]] = filter_params[vfield]
                    else:
                        errors[vfield] = f'{category} has no field {kfield} to compare with {vfield}'
                    filter_params.pop(vfield)


        queryset = queryset.filter(**filters)

        for m, specs in conf.HAVING_ALL_RELATIONS.items():
            for t in specs:
                if t[2] in filter_params:
                    if model == m:
                        for spec in filter_params[t[2]]:
                            queryset = queryset.intersection(
                                model.objects.filter(**{
                                    t[1]._meta.model_name + "__" + t[0]._meta.model_name: spec
                                })
                            )
                    else:
                        errors[t[2]] = f'{category} has no field to compare with {t[2]}'
                    filter_params.pop(t[2])

        for m, specs in conf.NUMBERED_HAVING_ALL_RELATIONS.items():
            for t in specs:
                if t[2] in filter_params:
                    if model == m:
                        for spec, num in filter_params[t[2]].items():
                            queryset = queryset.intersection(
                                model.objects.filter(**{
                                    t[1]._meta.model_name + "__" + t[0]._meta.model_name: spec,
                                    t[1]._meta.model_name + "__number__gte": num
                                })
                            )
                    else:
                        errors[t[2]] = f'{category} has no field to compare with {t[2]}'
                    filter_params.pop(t[2])


        for field in filter_params:
            errors[field] = 'unknown field'

        # for f in filter_params:
        #     filter_params[f] = str(filter_params[f])
        # return filter_params

        # for f in filters:
        #     filters[f] = str(filters[f])
        # return filters

        if error_check and errors != {}:
            raise ValueError(json.dumps(errors))

        return [item.to_json() for item in queryset]

    def get_specifications(specification: str) -> List[str]:
        return [
            {'name': str(spec), 'id': spec.id}
            for spec in pcc.SPECIFICATIONS[specification].objects.all()
        ]

    def get_belongings(belonging: str) -> List[str]:
        return [
            {'name': str(bel), **PCComponentsAPI.get_object_fields(bel)}
            for bel in pcc.BELONGINGS[belonging].objects.all()
        ]
    

    def add_item(category: str, params: Dict[str, Any]) -> int:
        model = pcc.item_class_by_category(category)
        item = model.objects.create(**params)
        return item.id
    
    def delete_item(pk: int) -> None:
        pcc.Item.objects.get(id=sample_id).delete()