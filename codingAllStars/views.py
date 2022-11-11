from django.http import HttpResponse
from django.shortcuts import render, redirect
from .scrapper import main
import asyncio, pandas,platform, mimetypes
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def scrape_data(request):

    category_url = request.GET.get('category')

    if category_url is not None:

        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        asyncio.run(main(category_url))

        df = pandas.read_csv('data.csv')
        return render(request, 'data.html', {"data": df.to_html()})
    
    return redirect("index")

def download_csv_file(request):

    fl_path = settings.BASE_DIR
    filename = "data.csv"

    full_fl_path  = None
    if platform.system() == "Windows":
        full_fl_path = str(fl_path)+"\\"+filename
    else:
        full_fl_path = str(fl_path)+"//"+filename

    with open(full_fl_path, "r+", encoding="utf-8") as fl:
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
