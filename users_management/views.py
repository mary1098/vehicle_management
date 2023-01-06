from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehicleSerializer, VehicleCreateSerializer, VehicleUpdateSerializer, VehicleGetSerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.

class SuperAdminApi(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        try:
            if 'filter' in request.GET:
                skip = request.GET['skip']
                number_rows = request.GET['take']
                page_number = int((int(skip) / int(number_rows)) + 1)
                filters = request.GET['filter']
                res = filters.strip('][').split(',')
                val = res[2].replace('"', '')
                vehicle_data = list(Vehicle.objects.filter(
                    Q(is_delete=0) & (Q(vehicle_id__icontains=val) | Q(vehicle_model__icontains=val))).order_by('-vehicle_id'))
                p = Paginator(vehicle_data, number_rows)
                user_page_data = p.page(page_number)
                data = user_page_data.object_list
                if data:
                    vehicle_dict = []
                    for i in data:
                        vehicle_object = {}
                        vehicle_object['vehicle_id'] = i.vehicle_id
                        vehicle_object['vehicle_number'] = i.vehicle_number
                        vehicle_object['vehicle_model'] = i.vehicle_model
                        vehicle_object['vehicle_type'] = i.vehicle_type
                        vehicle_object['vehicle_des'] = i.vehicle_des
                        vehicle_object['is_delete'] = i.is_delete
                        vehicle_object['is_active'] = i.is_active
                        vehicle_dict.append(vehicle_object)
                    return Response({
                        'status': True,
                        'data': vehicle_dict,
                        'totalCount': len(vehicle_data)
                    })
                else:
                    return Response({
                        'status': False,
                        'message': 'No data in To-Do List'
                    })
            else:
                if 'sort' in request.GET:
                    skip = request.GET['skip']
                    sort = request.GET['sort']
                    res = sort.strip('][}{').split(',')
                    val = res[0].replace('"', '')
                    val1 = res[1].replace('"', '')
                    desk = val1.split(':')[1]
                    if desk == 'false':
                        number_rows = request.GET['take']
                        page_number = int((int(skip) / int(number_rows)) + 1)
                        list_data = list(Vehicle.objects.filter(is_delete=0).order_by('-todo_id'))
                        p = Paginator(list_data, number_rows)
                        bin_page_data = p.page(page_number)
                        data = bin_page_data.object_list
                        data = Vehicle.objects.filter(todo_id__in=[object.todo_id for object in data]).order_by(
                            val.split(':')[1]).reverse()
                    else:
                        number_rows = request.GET['take']
                        page_number = int((int(skip) / int(number_rows)) + 1)
                        list_data = list(Vehicle.objects.filter(is_delete=0).order_by('-todo_id'))
                        p = Paginator(list_data, number_rows)
                        user_page_data = p.page(page_number)
                        data = user_page_data.object_list
                        data = Vehicle.objects.filter(todo_id__in=[object.company_id for object in data]).order_by(
                            val.split(':')[1])
                else:
                    skip = request.GET['skip']
                    number_rows = request.GET['take']
                    page_number = int((int(skip) / int(number_rows)) + 1)
                    vehicle_data = list(Vehicle.objects.filter(is_delete=0).order_by('-vehicle_id'))
                    p = Paginator(vehicle_data, number_rows)
                    user_page_data = p.page(page_number)
                    data = user_page_data.object_list
                    if data:
                        vehicle_dict = []
                        for i in data:
                            vehicle_object = {}
                            vehicle_object['vehicle_id'] = i.vehicle_id
                            vehicle_object['vehicle_number'] = i.vehicle_number
                            vehicle_object['vehicle_model'] = i.vehicle_model
                            vehicle_object['vehicle_type'] = i.vehicle_type
                            vehicle_object['vehicle_des'] = i.vehicle_des
                            vehicle_object['is_delete'] = i.is_delete
                            vehicle_object['is_active'] = i.is_active
                            vehicle_dict.append(vehicle_object)
                        return Response({
                            'status': True,
                            'data': vehicle_dict,
                            'totalCount': len(vehicle_data)
                        })
        except Exception as ex:
            return Response({
                'error': True,
                'Message': 'Internal error occurred'
            })


    def post(self, request):
        try:
            data = request.data
            if data:
                serialized_object = VehicleCreateSerializer(data=data)
                if serialized_object.is_valid():
                    vehicle_data = Vehicle(vehicle_des=data["vehicle_des"], vehicle_model=data["vehicle_model"],
                                           vehicle_number=data["vehicle_number"], vehicle_type=data['vehicle_type'],)
                    vehicle_data.save()
                    return Response({
                        'status': True,
                        'error': False,
                        'message': "Vehicle data created successfully!!"
                    })
                else:
                    return Response({
                        'status': False,
                        'error': True,
                        'message': "Please enter valid Vehicle data"
                    })
            else:
                return Response({
                    'status': False,
                    'error': True,
                    'message': " Please enter data"
                })
        except Exception as ex:
            print(ex)
            return Response({
                'status': False,
                'error': True,
                'message': "Internal server error occurred"
            })


    def put(self, request):
        try:
            data = request.data
            if data:
                serialized_object = VehicleUpdateSerializer(data=data)
                vehicle_objects = Vehicle.objects.filter(is_delete=0, vehicle_id=data["vehicle_id"])
                if vehicle_objects.count() != 0:
                    vehicle_detail = vehicle_objects[0]
                    if 'vehicle_number' in data:
                        vehicle_detail.vehicle_number = data["vehicle_number"]
                        vehicle_detail.vehicle_model = data["vehicle_model"]
                        vehicle_detail.vehicle_type = data["vehicle_type"]
                        vehicle_detail.vehicle_des = data["vehicle_des"]
                        vehicle_detail.save(force_update=True)
                        return Response({
                            'status': True,
                            'error': False,
                            'message': "Vehicle data updated successfully!!"
                        })
                    else:
                        return Response({
                            'status': False,
                            'error': True,
                            'message': "No such vehicle exists"
                        })
                else:
                    return Response({
                        'status': False,
                        'error': True,
                        'message': " Please enter data"
                    })
        except Exception as ex:
            print(ex)
            return Response({
                'status': False,
                'error': True,
                'message': "Internal server error occurred"
            })


    def delete(self, request):

        try:
            vehicle_id = request.query_params.get('vehicle_id', None)
            if vehicle_id is not None and vehicle_id.isnumeric():
                vehicle_objects = Vehicle.objects.filter(vehicle_id=int(vehicle_id))
                if vehicle_objects.count() != 0:
                    vehicle_number = vehicle_objects[0]
                    vehicle_number.is_active = 0
                    vehicle_number.is_delete = 1
                    vehicle_number.save(force_update=True)
                    return Response({
                        'status': True,
                        'error': False,
                        'message': "Vehicle deleted successfully"
                    })
                else:
                    return Response({
                        'status': False,
                        'error': True,
                        'message': "No such vehicle exists"
                    })
            else:
                return Response({
                    'status': False,
                    'error': True,
                    'message': "Please enter valid  vehicle id"
                })
        except Exception as ex:
            print(ex)
            return Response({
                'status': False,
                'error': True,
                'message': "Internal server error occurred"
            })


class AdminApi(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        try:
            if 'filter' in request.GET:
                skip = request.GET['skip']
                number_rows = request.GET['take']
                page_number = int((int(skip) / int(number_rows)) + 1)
                filters = request.GET['filter']
                res = filters.strip('][').split(',')
                val = res[2].replace('"', '')
                vehicle_data = list(Vehicle.objects.filter(
                    Q(is_delete=0) & (Q(vehicle_id__icontains=val) | Q(vehicle_model__icontains=val))).order_by('-vehicle_id'))
                p = Paginator(vehicle_data, number_rows)
                user_page_data = p.page(page_number)
                data = user_page_data.object_list
                if data:
                    vehicle_dict = []
                    for i in data:
                        vehicle_object = {}
                        vehicle_object['vehicle_id'] = i.vehicle_id
                        vehicle_object['vehicle_number'] = i.vehicle_number
                        vehicle_object['vehicle_model'] = i.vehicle_model
                        vehicle_object['vehicle_type'] = i.vehicle_type
                        vehicle_object['vehicle_des'] = i.vehicle_des
                        vehicle_object['is_delete'] = i.is_delete
                        vehicle_object['is_active'] = i.is_active
                        vehicle_dict.append(vehicle_object)
                    return Response({
                        'status': True,
                        'data': vehicle_dict,
                        'totalCount': len(vehicle_data)
                    })
                else:
                    return Response({
                        'status': False,
                        'message': 'No data in To-Do List'
                    })
            else:
                if 'sort' in request.GET:
                    skip = request.GET['skip']
                    sort = request.GET['sort']
                    res = sort.strip('][}{').split(',')
                    val = res[0].replace('"', '')
                    val1 = res[1].replace('"', '')
                    desk = val1.split(':')[1]
                    if desk == 'false':
                        number_rows = request.GET['take']
                        page_number = int((int(skip) / int(number_rows)) + 1)
                        list_data = list(Vehicle.objects.filter(is_delete=0).order_by('-todo_id'))
                        p = Paginator(list_data, number_rows)
                        bin_page_data = p.page(page_number)
                        data = bin_page_data.object_list
                        data = Vehicle.objects.filter(todo_id__in=[object.todo_id for object in data]).order_by(
                            val.split(':')[1]).reverse()
                    else:
                        number_rows = request.GET['take']
                        page_number = int((int(skip) / int(number_rows)) + 1)
                        list_data = list(Vehicle.objects.filter(is_delete=0).order_by('-todo_id'))
                        p = Paginator(list_data, number_rows)
                        user_page_data = p.page(page_number)
                        data = user_page_data.object_list
                        data = Vehicle.objects.filter(todo_id__in=[object.company_id for object in data]).order_by(
                            val.split(':')[1])
                else:
                    skip = request.GET['skip']
                    number_rows = request.GET['take']
                    page_number = int((int(skip) / int(number_rows)) + 1)
                    vehicle_data = list(Vehicle.objects.filter(is_delete=0).order_by('-vehicle_id'))
                    p = Paginator(vehicle_data, number_rows)
                    user_page_data = p.page(page_number)
                    data = user_page_data.object_list
                    if data:
                        vehicle_dict = []
                        for i in data:
                            vehicle_object = {}
                            vehicle_object['vehicle_id'] = i.vehicle_id
                            vehicle_object['vehicle_number'] = i.vehicle_number
                            vehicle_object['vehicle_model'] = i.vehicle_model
                            vehicle_object['vehicle_type'] = i.vehicle_type
                            vehicle_object['vehicle_des'] = i.vehicle_des
                            vehicle_object['is_delete'] = i.is_delete
                            vehicle_object['is_active'] = i.is_active
                            vehicle_dict.append(vehicle_object)
                        return Response({
                            'status': True,
                            'data': vehicle_dict,
                            'totalCount': len(vehicle_data)
                        })
        except Exception as ex:
            return Response({
                'error': True,
                'Message': 'Internal error occurred'
            })


    def put(self, request):
        try:
            data = request.data
            if data:
                serialized_object = VehicleUpdateSerializer(data=data)
                vehicle_objects = Vehicle.objects.filter(is_delete=0, vehicle_id=data["vehicle_id"])
                if vehicle_objects.count() != 0:
                    vehicle_detail = vehicle_objects[0]
                    if 'vehicle_number' in data:
                        vehicle_detail.vehicle_number = data["vehicle_number"]
                        vehicle_detail.vehicle_model = data["vehicle_model"]
                        vehicle_detail.vehicle_type = data["vehicle_type"]
                        vehicle_detail.vehicle_des = data["vehicle_des"]
                        vehicle_detail.save(force_update=True)
                        return Response({
                            'status': True,
                            'error': False,
                            'message': "Vehicle data updated successfully!!"
                        })
                    else:
                        return Response({
                            'status': False,
                            'error': True,
                            'message': "No such vehicle exists"
                        })
                else:
                    return Response({
                        'status': False,
                        'error': True,
                        'message': " Please enter data"
                    })
        except Exception as ex:
            print(ex)
            return Response({
                'status': False,
                'error': True,
                'message': "Internal server error occurred"
            })


class UserApi(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        try:
            if 'filter' in request.GET:
                skip = request.GET['skip']
                number_rows = request.GET['take']
                page_number = int((int(skip) / int(number_rows)) + 1)
                filters = request.GET['filter']
                res = filters.strip('][').split(',')
                val = res[2].replace('"', '')
                vehicle_data = list(Vehicle.objects.filter(
                    Q(is_delete=0) & (Q(vehicle_id__icontains=val) | Q(vehicle_model__icontains=val))).order_by('-vehicle_id'))
                p = Paginator(vehicle_data, number_rows)
                user_page_data = p.page(page_number)
                data = user_page_data.object_list
                if data:
                    vehicle_dict = []
                    for i in data:
                        vehicle_object = {}
                        vehicle_object['vehicle_id'] = i.vehicle_id
                        vehicle_object['vehicle_number'] = i.vehicle_number
                        vehicle_object['vehicle_model'] = i.vehicle_model
                        vehicle_object['vehicle_type'] = i.vehicle_type
                        vehicle_object['vehicle_des'] = i.vehicle_des
                        vehicle_object['is_delete'] = i.is_delete
                        vehicle_object['is_active'] = i.is_active
                        vehicle_dict.append(vehicle_object)
                    return Response({
                        'status': True,
                        'data': vehicle_dict,
                        'totalCount': len(vehicle_data)
                    })
                else:
                    return Response({
                        'status': False,
                        'message': 'No data in To-Do List'
                    })
            else:
                if 'sort' in request.GET:
                    skip = request.GET['skip']
                    sort = request.GET['sort']
                    res = sort.strip('][}{').split(',')
                    val = res[0].replace('"', '')
                    val1 = res[1].replace('"', '')
                    desk = val1.split(':')[1]
                    if desk == 'false':
                        number_rows = request.GET['take']
                        page_number = int((int(skip) / int(number_rows)) + 1)
                        list_data = list(Vehicle.objects.filter(is_delete=0).order_by('-todo_id'))
                        p = Paginator(list_data, number_rows)
                        bin_page_data = p.page(page_number)
                        data = bin_page_data.object_list
                        data = Vehicle.objects.filter(todo_id__in=[object.todo_id for object in data]).order_by(
                            val.split(':')[1]).reverse()
                    else:
                        number_rows = request.GET['take']
                        page_number = int((int(skip) / int(number_rows)) + 1)
                        list_data = list(Vehicle.objects.filter(is_delete=0).order_by('-todo_id'))
                        p = Paginator(list_data, number_rows)
                        user_page_data = p.page(page_number)
                        data = user_page_data.object_list
                        data = Vehicle.objects.filter(todo_id__in=[object.company_id for object in data]).order_by(
                            val.split(':')[1])
                else:
                    skip = request.GET['skip']
                    number_rows = request.GET['take']
                    page_number = int((int(skip) / int(number_rows)) + 1)
                    vehicle_data = list(Vehicle.objects.filter(is_delete=0).order_by('-vehicle_id'))
                    p = Paginator(vehicle_data, number_rows)
                    user_page_data = p.page(page_number)
                    data = user_page_data.object_list
                    if data:
                        vehicle_dict = []
                        for i in data:
                            vehicle_object = {}
                            vehicle_object['vehicle_id'] = i.vehicle_id
                            vehicle_object['vehicle_number'] = i.vehicle_number
                            vehicle_object['vehicle_model'] = i.vehicle_model
                            vehicle_object['vehicle_type'] = i.vehicle_type
                            vehicle_object['vehicle_des'] = i.vehicle_des
                            vehicle_object['is_delete'] = i.is_delete
                            vehicle_object['is_active'] = i.is_active
                            vehicle_dict.append(vehicle_object)
                        return Response({
                            'status': True,
                            'data': vehicle_dict,
                            'totalCount': len(vehicle_data)
                        })
        except Exception as ex:
            return Response({
                'error': True,
                'Message': 'Internal error occurred'
            })

