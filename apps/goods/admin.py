from django.contrib import admin
from apps.goods.models import GoodsType,IndexPromotionBanner,GoodsSKU,Goods,GoodsImage,IndexGoodsBanner,IndexTypeGoodsBanner

class IndexPromotionBannerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''数据新增或者更新调用'''
        super().save_model(request,obj,form,change)
        #使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()

    def delete_model(self, request, obj):
        '''删除表中数据时调用'''
        super().delete_model(request,obj)
        # 使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()
class GoodsTypeAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''数据新增或者更新调用'''
        super().save_model(request,obj,form,change)
        #使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()

    def delete_model(self, request, obj):
        '''删除表中数据时调用'''
        super().delete_model(request,obj)
        # 使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()
class GoodsSKUAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''数据新增或者更新调用'''
        super().save_model(request,obj,form,change)
        #使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()

    def delete_model(self, request, obj):
        '''删除表中数据时调用'''
        super().delete_model(request,obj)
        # 使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()
class GoodsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''数据新增或者更新调用'''
        super().save_model(request,obj,form,change)
        #使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()

    def delete_model(self, request, obj):
        '''删除表中数据时调用'''
        super().delete_model(request,obj)
        # 使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()
class GoodsImageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''数据新增或者更新调用'''
        super().save_model(request,obj,form,change)
        #使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()

    def delete_model(self, request, obj):
        '''删除表中数据时调用'''
        super().delete_model(request,obj)
        # 使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()
class IndexGoodsBannerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''数据新增或者更新调用'''
        super().save_model(request,obj,form,change)
        #使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()

    def delete_model(self, request, obj):
        '''删除表中数据时调用'''
        super().delete_model(request,obj)
        # 使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()
class IndexTypeGoodsBannerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''数据新增或者更新调用'''
        super().save_model(request,obj,form,change)
        #使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()

    def delete_model(self, request, obj):
        '''删除表中数据时调用'''
        super().delete_model(request,obj)
        # 使用celery,异步重新生成静态页面
        from celery_tasks.tasks import gemerate_static_index_html
        gemerate_static_index_html.delay()


#當用戶修改表內容事調用類對內容進行修改
admin.site.register(GoodsType,GoodsTypeAdmin)
admin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin)
admin.site.register(GoodsSKU,GoodsSKUAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(GoodsImage,GoodsImageAdmin)
admin.site.register(IndexGoodsBanner,IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner,IndexTypeGoodsBannerAdmin)



# Register your models here.


