# encoding:utf-8

class ConfigSwagger:
    SWAGGER = {
        'title': 'Blog API',                          # API标题
        'version': '1.0.0',                          # API版本号
        'openapi': '3.0.2',                          # 显式声明使用OpenAPI 3.0
        'uiversion': 3,                              # 使用Swagger UI 3
        'specs_route': '/apidocs/',                  # 文档路由地址
        'description': '这是一个使用Flasgger生成的个人博客(Vue3框架)的API调用文档。', # 文档描述
    }