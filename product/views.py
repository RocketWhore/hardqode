from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from product.models import Product, Accessible, Group, Lesson
from product.serializers import ProductSerializer, LessonSerializer


class ProductsViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_accessible=True).annotate(num_lessons=Count('lessons'))
    serializer_class = ProductSerializer

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def get_access(self, request, pk):
        if Accessible.objects.filter(user=request.user, product_id=pk).exists():
            raise ValidationError('Подписка уже существует')
        Accessible.objects.create(user=request.user, product_id=pk)
        product = self.get_object()
        count_groups = product.groups.count()
        if count_groups == 0:
            group = Group.objects.create(title='группа 1', product=product)
            group.students.add(request.user)
            return Response('Доступ получен')

        groups = product.groups.annotate(num_students=Count('students')).filter(num_students__lte=product.max_students)
        group = groups.firts()
        if group is not None:
            group.students.add(self.request.user)
            return Response('Доступ получен')

        group = Group.objects.create(title=f'группа {count_groups + 1}', product=product)
        group.students.add(request.user)
        return Response('Доступ получен')

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def lessons(self, request, pk):
        if not Accessible.objects.filter(user=request.user, product_id=pk).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        lessons = Lesson.objects.select_related('product').filter(product_id=pk)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
