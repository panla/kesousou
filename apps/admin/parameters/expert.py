# -*- encoding=utf-8 -*-

from drf_yasg import openapi

expert_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='name or organization or major or research_areas or keywords',
        type=openapi.TYPE_STRING
    ),
]

expert_create_params = openapi.Schema(
    title='expert', description='创建expert',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(description='专家姓名', type=openapi.TYPE_STRING),
        'organization': openapi.Schema(description='所属机构', type=openapi.TYPE_STRING),
        'department': openapi.Schema(description='学院/学部/研究所/部门', type=openapi.TYPE_STRING),
        'keywords': openapi.Schema(
            description='关键词', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'personal_introduction': openapi.Schema(description='个人简介', type=openapi.TYPE_STRING),
        'birth': openapi.Schema(description='出生日期', type=openapi.TYPE_STRING),
        'info_link': openapi.Schema(description='专家信息链接', type=openapi.TYPE_STRING),
        'post': openapi.Schema(description='职务', type=openapi.TYPE_STRING),
        'title': openapi.Schema(description='职称', type=openapi.TYPE_STRING),
        'degree': openapi.Schema(description='学历/学位', type=openapi.TYPE_STRING),
        'honorary_titles': openapi.Schema(description='荣誉称号', type=openapi.TYPE_STRING),
        'graduated_from': openapi.Schema(description='毕业院校', type=openapi.TYPE_STRING),
        'major': openapi.Schema(description='专业/学科', type=openapi.TYPE_STRING),
        'research_areas': openapi.Schema(description='研究方向', type=openapi.TYPE_STRING),
        'projects': openapi.Schema(description='成果', type=openapi.TYPE_STRING),
        'contact': openapi.Schema(description='联系方式', type=openapi.TYPE_STRING),
        'province': openapi.Schema(description='省份', type=openapi.TYPE_STRING),
        'city': openapi.Schema(description='城市', type=openapi.TYPE_STRING),
        'address': openapi.Schema(description='办公地点', type=openapi.TYPE_STRING),
        'origins': openapi.Schema(description='数据来源', type=openapi.TYPE_STRING),
    }
)

expert_update_params = openapi.Schema(
    title='expert', description='更新expert',
    type=openapi.TYPE_OBJECT,
    properties=expert_create_params.properties
)
