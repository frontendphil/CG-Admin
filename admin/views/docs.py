from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response

from admin.models import Doctor
from admin.decorators import require_login
from admin.templatetags.admin_extras import get_query

@require_login
def search(request):
    query = request.GET.get("query")

    if query:
        q = get_query(query, ["name", "key", "address__street", "address__city"])

        docs_list = Doctor.objects.filter(q)
    else:
        docs_list = Doctor.objects.all()

    paginator = Paginator(docs_list, 25)

    page = request.GET.get("page")

    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    return render_to_response("docs/search.html",
                              locals(),
                              context_instance=RequestContext(request))

@require_login
def show(request, id):
    pass

@require_login
def delete(request, id):
    pass

@require_login
def edit(request, id):
    return render_to_response("docs/edit.html",
                              locals(),
                              context_instance=RequestContext(request))