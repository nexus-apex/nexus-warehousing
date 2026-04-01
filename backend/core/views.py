import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Zone, InventoryItem, PickList


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['zone_count'] = Zone.objects.count()
    ctx['zone_receiving'] = Zone.objects.filter(zone_type='receiving').count()
    ctx['zone_storage'] = Zone.objects.filter(zone_type='storage').count()
    ctx['zone_picking'] = Zone.objects.filter(zone_type='picking').count()
    ctx['zone_total_utilization'] = Zone.objects.aggregate(t=Sum('utilization'))['t'] or 0
    ctx['inventoryitem_count'] = InventoryItem.objects.count()
    ctx['inventoryitem_available'] = InventoryItem.objects.filter(status='available').count()
    ctx['inventoryitem_reserved'] = InventoryItem.objects.filter(status='reserved').count()
    ctx['inventoryitem_damaged'] = InventoryItem.objects.filter(status='damaged').count()
    ctx['picklist_count'] = PickList.objects.count()
    ctx['picklist_pending'] = PickList.objects.filter(status='pending').count()
    ctx['picklist_in_progress'] = PickList.objects.filter(status='in_progress').count()
    ctx['picklist_completed'] = PickList.objects.filter(status='completed').count()
    ctx['recent'] = Zone.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def zone_list(request):
    qs = Zone.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(zone_type=status_filter)
    return render(request, 'zone_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def zone_create(request):
    if request.method == 'POST':
        obj = Zone()
        obj.name = request.POST.get('name', '')
        obj.warehouse = request.POST.get('warehouse', '')
        obj.zone_type = request.POST.get('zone_type', '')
        obj.capacity = request.POST.get('capacity') or 0
        obj.utilization = request.POST.get('utilization') or 0
        obj.temperature = request.POST.get('temperature', '')
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/zones/')
    return render(request, 'zone_form.html', {'editing': False})


@login_required
def zone_edit(request, pk):
    obj = get_object_or_404(Zone, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.warehouse = request.POST.get('warehouse', '')
        obj.zone_type = request.POST.get('zone_type', '')
        obj.capacity = request.POST.get('capacity') or 0
        obj.utilization = request.POST.get('utilization') or 0
        obj.temperature = request.POST.get('temperature', '')
        obj.active = request.POST.get('active') == 'on'
        obj.save()
        return redirect('/zones/')
    return render(request, 'zone_form.html', {'record': obj, 'editing': True})


@login_required
def zone_delete(request, pk):
    obj = get_object_or_404(Zone, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/zones/')


@login_required
def inventoryitem_list(request):
    qs = InventoryItem.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'inventoryitem_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def inventoryitem_create(request):
    if request.method == 'POST':
        obj = InventoryItem()
        obj.name = request.POST.get('name', '')
        obj.sku = request.POST.get('sku', '')
        obj.zone_name = request.POST.get('zone_name', '')
        obj.quantity = request.POST.get('quantity') or 0
        obj.lot_number = request.POST.get('lot_number', '')
        obj.expiry_date = request.POST.get('expiry_date') or None
        obj.last_counted = request.POST.get('last_counted') or None
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/inventoryitems/')
    return render(request, 'inventoryitem_form.html', {'editing': False})


@login_required
def inventoryitem_edit(request, pk):
    obj = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.sku = request.POST.get('sku', '')
        obj.zone_name = request.POST.get('zone_name', '')
        obj.quantity = request.POST.get('quantity') or 0
        obj.lot_number = request.POST.get('lot_number', '')
        obj.expiry_date = request.POST.get('expiry_date') or None
        obj.last_counted = request.POST.get('last_counted') or None
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/inventoryitems/')
    return render(request, 'inventoryitem_form.html', {'record': obj, 'editing': True})


@login_required
def inventoryitem_delete(request, pk):
    obj = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/inventoryitems/')


@login_required
def picklist_list(request):
    qs = PickList.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(pick_number__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'picklist_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def picklist_create(request):
    if request.method == 'POST':
        obj = PickList()
        obj.pick_number = request.POST.get('pick_number', '')
        obj.order_ref = request.POST.get('order_ref', '')
        obj.zone_name = request.POST.get('zone_name', '')
        obj.items_count = request.POST.get('items_count') or 0
        obj.status = request.POST.get('status', '')
        obj.assigned_to = request.POST.get('assigned_to', '')
        obj.created_date = request.POST.get('created_date') or None
        obj.save()
        return redirect('/picklists/')
    return render(request, 'picklist_form.html', {'editing': False})


@login_required
def picklist_edit(request, pk):
    obj = get_object_or_404(PickList, pk=pk)
    if request.method == 'POST':
        obj.pick_number = request.POST.get('pick_number', '')
        obj.order_ref = request.POST.get('order_ref', '')
        obj.zone_name = request.POST.get('zone_name', '')
        obj.items_count = request.POST.get('items_count') or 0
        obj.status = request.POST.get('status', '')
        obj.assigned_to = request.POST.get('assigned_to', '')
        obj.created_date = request.POST.get('created_date') or None
        obj.save()
        return redirect('/picklists/')
    return render(request, 'picklist_form.html', {'record': obj, 'editing': True})


@login_required
def picklist_delete(request, pk):
    obj = get_object_or_404(PickList, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/picklists/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['zone_count'] = Zone.objects.count()
    data['inventoryitem_count'] = InventoryItem.objects.count()
    data['picklist_count'] = PickList.objects.count()
    return JsonResponse(data)
