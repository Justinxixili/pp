# my_pp/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from toolz.curried import reduce

from .models import Patent, Company, InfringementReport
from .services.analyzer import InfringementAnalyzer
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


class HomeView(TemplateView):
    template_name = 'index.html'


def analyze_infringement(request):
    if request.method == 'POST':
        patent_id = request.POST.get('patent_id')
        company_name = request.POST.get('company_name')

        try:
            # 首先获取专利和公司对象
            try:
                patent = Patent.objects.get(patent_id=patent_id)
            except Patent.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Patent with ID {patent_id} not found'
                })

            try:
                company = Company.objects.get(name=company_name)
            except Company.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Company with name {company_name} not found'
                })

            # 进行分析
            analyzer = InfringementAnalyzer()
            result = analyzer.analyze(patent_id, company_name)
            print(result)
            # 保存分析结果
            report = InfringementReport.objects.create(
                patent=patent,  # 使用专利对象
                company=company,  # 使用公司对象
                top_infringing_products=result.get('top_infringing_products', []),
                overall_risk_assessment=result.get('overall_risk_assessment', '')
            )

            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            import traceback
            print(traceback.format_exc())  # 打印详细错误信息到控制台
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })


# 添加一个用于检查数据的视图函数（可选）
def check_data(request):
    """用于检查数据库中的数据状态"""
    try:
        patents = Patent.objects.all()
        companies = Company.objects.all()
        print(patents.count())
        print(companies.count())
        print(list(patents.values('patent_id', 'title')[:3]))
        print(list(companies.values('name')[:3]))
        return JsonResponse({
            'status': 'success',
            'data': {
                'patents_count': patents.count(),
                'patents_sample': list(patents.values('patent_id', 'title')[:3]),
                'companies_count': companies.count(),
                'companies_sample': list(companies.values('name')[:3])
            }
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
def login_data(request):
    if request.GET.get('company_name'):
        patent_id = request.GET.get('patent_id')
        company_name = request.GET.get('company_name')
        print(patent_id, company_name)
        try:
            # 首先获取专利和公司对象
            try:
                patent = Patent.objects.get(patent_id=patent_id)
            except Patent.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Patent with ID {patent_id} not found'
                })

            try:
                company = Company.objects.get(name=company_name)
            except Company.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Company with name {company_name} not found'
                })

            # 进行分析
            analyzer = InfringementAnalyzer()
            result = analyzer.analyze(patent_id, company_name)
            print(result)
            # 保存分析结果
            report = InfringementReport.objects.create(
                patent=patent,  # 使用专利对象
                company=company,  # 使用公司对象
                top_infringing_products=result.get('top_infringing_products', []),
                overall_risk_assessment=result.get('overall_risk_assessment', '')
            )

            return render(request,'index_two.html',{'status': 'success', 'data': result,'patent_id':patent_id,'company_name':company_name},)
        except Exception as e:
            import traceback
            print(traceback.format_exc())  # 打印详细错误信息到控制台
            return render(request,'index_two.html',{
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            })
    else:
        return render(request,'index_two.html')
def index_two(request):
    return render(request,'index_two.html',)