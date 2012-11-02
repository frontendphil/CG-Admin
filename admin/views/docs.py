from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from admin.models import Doctor
from admin.decorators import require_login
from admin.templatetags.admin_extras import get_query
from admin.forms import DoctorForm

@require_login
def search(request):
    query = request.GET.get("query")

    if query:
        return redirect("list_docs", query=query, page=1)

    return redirect("list_docs_page", page=1)

@require_login
def list(request, query=None, page=1):
    if query and query == "None":
        return redirect("list_docs_page", page=page)

    if query:
        q = get_query(query, ["name", "key", "address__street", "address__city"])

        docs_list = Doctor.objects.filter(q)
    else:
        docs_list = Doctor.objects.all()

    paginator = Paginator(docs_list, 25)
    
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
@require_POST
def delete(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    doctor.delete()

    follow = request.GET.get("redirect", None)

    # TODO: check that!
    if follow:
        return redirect(follow)


@require_login
def edit(request, id):
    doc = get_object_or_404(Doctor, pk=id)

    if request.method == "POST":
        pass
    else:
        form = DoctorForm.from_doctor(doc)

    return render_to_response("docs/edit.html",
                              locals(),
                              context_instance=RequestContext(request))