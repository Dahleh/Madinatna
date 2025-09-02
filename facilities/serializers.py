from rest_framework import serializers
from .models import Category, Cluster, Facility, FacilityImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ["id", "name", "description"]


class FacilityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityImage
        fields = ["id", "image", "caption", "order"]
        read_only_fields = ["id"]


class FacilitySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source="category", queryset=Category.objects.all(), write_only=True)
    cluster = ClusterSerializer(read_only=True)
    cluster_id = serializers.PrimaryKeyRelatedField(source="cluster", queryset=Cluster.objects.all(), write_only=True)
    images = FacilityImageSerializer(many=True, read_only=True)

    class Meta:
        model = Facility
        fields = [
            "id",
            "name",
            "description",
            "category",
            "category_id",
            "cluster",
            "cluster_id",
            "address",
            "phone",
            "email",
            "is_active",
            "owner",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class FacilityWriteSerializer(FacilitySerializer):
    images = FacilityImageSerializer(many=True, write_only=True, required=False)

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        facility = super().create(validated_data)
        for idx, img in enumerate(images_data):
            FacilityImage.objects.create(facility=facility, order=img.get("order", idx), **img)
        return facility

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", None)
        facility = super().update(instance, validated_data)
        if images_data is not None:
            facility.images.all().delete()
            for idx, img in enumerate(images_data):
                FacilityImage.objects.create(facility=facility, order=img.get("order", idx), **img)
        return facility
