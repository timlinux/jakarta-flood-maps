# coding=utf-8
"""Views."""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import os

from flood_mapper.utilities.utilities import create_reports_directories


def reports(request):
    available_reports = {}
    reports_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        os.path.pardir,
        'reports'))
    if not os.path.exists(reports_dir):
        create_reports_directories()

    for (report_type, extention) in [
            ('pdf', '.pdf'),
            ('sqlite', '.sqlite'),
            ('shp', '.zip'),
            ('kml', '.kml'),
            ('csv', '.csv')]:
        report_type_dir = os.path.join(reports_dir, report_type)
        available_reports[report_type] = {}
        for report_period in ['6h', '24h']:
            report_type_time_period_dir = os.path.join(
                report_type_dir, report_period)
            directory_content = os.listdir(
                report_type_time_period_dir)
            available_reports[report_type][report_period] = [
                f for f in directory_content if f.endswith(extention)
            ]
            available_reports[report_type][report_period].sort(reverse=True)
            # Only show the first 10 reports as options in the drop down
            available_reports[report_type][report_period] = (
                available_reports[report_type][report_period][:10]
            )

    return render(
        request,
        'flood_mapper/reports.html',
        context_instance=RequestContext(
            request, {'reports': available_reports}))
