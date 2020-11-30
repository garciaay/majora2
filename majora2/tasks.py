# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task, current_task
from . import models
from . import serializers
from . import resty_serializers
from . import util

from django.db.models import Q

import datetime

from tatl.models import TatlVerb, TatlRequest

@shared_task
def structify_pags(api_o):
    # Return everything?
    api_o["get"] = {}
    api_o["get"]["result"] = serializers.PAGQCSerializer(models.PAGQualityReportEquivalenceGroup.objects.select_related('pag').prefetch_related('pag__tagged_artifacts').all(), many=True).data
    return api_o

@shared_task
def task_get_sequencing_faster(request, api_o, json_data, user=None, **kwargs):
    run_ids = models.DNASequencingProcess.objects.all().values_list("id", flat=True)
    lib_ids = models.MajoraArtifactProcessRecord.objects.filter(process_id__in=run_ids).values_list("in_artifact__id", flat=True).distinct()
    biosample_ids = models.MajoraArtifactProcessRecord.objects.filter(out_artifact__id__in=lib_ids).values_list("in_artifact__id", flat=True).distinct()

    try:
        api_o["get"] = {}
        api_o["get"]["result"] = {
            "biosamples": [x.as_struct() for x in models.BiosampleArtifact.objects.filter(id__in=biosample_ids).prefetch_related('created')],
            "runs": [x.as_struct(deep=False) for x in models.DNASequencingProcess.objects.filter(id__in=run_ids)],
            "libraries": [x.as_struct(deep=False) for x in models.LibraryArtifact.objects.filter(id__in=lib_ids)],
        }
        api_o["get"]["count"] = (run_ids.count(), lib_ids.count(), biosample_ids.count())
    except Exception as e:
        api_o["errors"] += 1
        api_o["messages"].append(str(e))
    return api_o


@shared_task
def task_get_sequencing(request, api_o, json_data, user=None, **kwargs):
    run_names = json_data.get("run_name")
    if not run_names:
        api_o["messages"].append("'run_name' key missing or empty")
        api_o["errors"] += 1
        return

    if len(run_names) == 1 and run_names[0] == "*":
        #TODO Cannot check staff status here, relies on checking in the calling view.
        run_names = [run["run_name"] for run in models.DNASequencingProcess.objects.all().values("run_name")]

    runs = {}
    for run_name in run_names:
        try:
            process = models.DNASequencingProcess.objects.get(run_name=run_name)
        except Exception as e:
            api_o["warnings"] += 1
            api_o["ignored"].append(run_name)
            continue

        try:
            runs[process.run_name] = process.as_struct()
        except Exception as e:
            api_o["errors"] += 1
            api_o["messages"].append(str(e))
            continue

    try:
        api_o["get"] = {}
        api_o["get"]["result"] = runs
        api_o["get"]["count"] = len(runs)
    except Exception as e:
        api_o["errors"] += 1
        api_o["messages"].append(str(e))
    return api_o


@shared_task
def task_get_pag_by_qc_faster(request, api_o, json_data, user=None, **kwargs):
    test_name = json_data.get("test_name")

    if not test_name or len(test_name) == 0:
        api_o["messages"].append("'test_name', key missing or empty")
        api_o["errors"] += 1
        return
    t_group = models.PAGQualityTestEquivalenceGroup.objects.filter(slug=test_name).first()
    if not t_group:
        api_o["messages"].append("Invalid 'test_name'")
        api_o["ignored"].append(test_name)
        api_o["errors"] += 1
        return

    base_q = Q(
        groups__publishedartifactgroup__isnull=False, # has PAG
        groups__publishedartifactgroup__quality_groups__test_group=t_group, # Has result for this QC test
        groups__publishedartifactgroup__is_latest=True, # Is latest and
        groups__publishedartifactgroup__is_suppressed=False) # not suppressed for bad reasons

    if json_data.get("pass") and json_data.get("fail"):
        status_q= Q() # Should basically be NOP
    elif json_data.get("pass"):
        status_q = Q(groups__publishedartifactgroup__quality_groups__is_pass=True)
    elif json_data.get("fail"):
        status_q = Q(groups__publishedartifactgroup__quality_groups__is_pass=False)
    else:
        pass

    # Perform the query
    artifacts = models.DigitalResourceArtifact.objects.filter(base_q, status_q)

    # Collapse into list items
    artifacts = list(artifacts.values_list('groups__publishedartifactgroup__published_name', 'current_kind', 'current_path', 'current_hash', 'current_size', 'groups__publishedartifactgroup__quality_groups__is_pass'))

    try:
        api_o["get"] = {}
        api_o["get"]["result"] = artifacts
        api_o["get"]["count"] = len(artifacts)
    except Exception as e:
        api_o["errors"] += 1
        api_o["messages"].append(str(e))
    return api_o

@shared_task
def task_get_pag_by_qc(request, api_o, json_data, user=None, **kwargs):
    test_name = json_data.get("test_name")
    dra_current_kind = json_data.get("dra_current_kind")

    if not test_name or len(test_name) == 0:
        api_o["messages"].append("'test_name', key missing or empty")
        api_o["errors"] += 1
        return
    t_group = models.PAGQualityTestEquivalenceGroup.objects.filter(slug=test_name).first()
    if not t_group:
        api_o["messages"].append("Invalid 'test_name'")
        api_o["ignored"].append(test_name)
        api_o["errors"] += 1
        return

    reports = models.PAGQualityReportEquivalenceGroup.objects.filter(test_group=t_group, pag__is_latest=True, pag__is_suppressed=False)

    if json_data.get("published_date"):
        try:
            gt_date = datetime.datetime.strptime(json_data.get("published_after", ""), "%Y-%m-%d")
            reports = reports.filter(pag__published_date__gt=gt_date)
        except Exception as e:
            api_o["errors"] += 1
            api_o["messages"].append(str(e))

    if json_data.get("pass") and json_data.get("fail"):
        pass
    elif json_data.get("pass"):
        reports = reports.filter(is_pass=True)
    elif json_data.get("fail"):
        reports = reports.filter(is_pass=False)
    else:
        pass

    # Return only PAGs with the service name, otherwise use the is_pbulic shortcut
    if json_data.get("public") and json_data.get("private"):
        if json_data.get("service_name"):
            api_o["messages"].append("service_name is ignored with both public and private")
        pass
    elif json_data.get("public"):
        if json_data.get("service_name"):
            reports = reports.filter(pag__accessions__service=json_data.get("service_name"), pag__accessions__is_public=True)
        else:
            reports = reports.filter(pag__is_public=True)
    elif json_data.get("private"):
        if json_data.get("service_name"):
            # Exclude any PAG that has this service name (public or not)
            # Private means unsubmitted in this context basically
            reports = reports.filter(~Q(pag__accessions__service=json_data.get("service_name")))
        else:
            reports = reports.filter(pag__is_public=False)
    else:
        if json_data.get("service_name"):
            api_o["messages"].append("service_name is ignored without public or private")
        pass



    try:
        api_o["get"] = {}
        api_o["get"]["result"] = serializers.PAGQCSerializer(reports.select_related('pag').prefetch_related('pag__tagged_artifacts').all(), many=True).data
        api_o["get"]["count"] = len(reports)
    except Exception as e:
        api_o["errors"] += 1
        api_o["messages"].append(str(e))
    return api_o

@shared_task
def task_get_pag_by_qc_v3(pag_ids, context={}):
    queryset = models.PublishedArtifactGroup.objects.filter(id__in=pag_ids)
    serializer = resty_serializers.RestyPublishedArtifactGroupSerializer(queryset, many=True, context=context)

    api_o = {
        "data": serializer.data,
    }

    return api_o

@shared_task
def task_get_mdv_v3(ids, context={}, **kwargs):
    from django.apps import apps

    mdv = models.MajoraDataview.objects.get(code_name=context["mdv"])

    treq = None
    if kwargs.get("response_uuid"):
        treq = TatlRequest.objects.get(response_uuid=kwargs.get("response_uuid"))
        TatlVerb(request=treq, verb="RETRIEVE", content_object=mdv).save()

    model = apps.get_model("majora2", mdv.entry_point)
    queryset = model.objects.filter(id__in=ids)

    context["mdv_fields"] = util.get_mdv_fields(context["mdv"])
    serializer = model.get_resty_serializer()(queryset, many=True, context=context)

    api_o = {
        "data": serializer.data,
    }


    return api_o
