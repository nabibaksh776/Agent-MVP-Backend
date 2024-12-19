from rest_framework import serializers
from .models import Customer, Agent, AgentDocument, Visitor, Chat, SalesTechnique,SalesTechniquesDocument


# Serializer for Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "firstName", "lastName", "email", "phone_number", "role"]


# Serializer for Agent
class AgentSerializer(serializers.ModelSerializer):
    # Serialize the customer relationship
    customer = CustomerSerializer(read_only=True)
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = "__all__"

    def get_documents(self, obj):
        # Return all documents related to the agent
        documents = AgentDocument.objects.filter(agent=obj)
        return AgentDocumentSerializer(documents, many=True).data


# Serializer for AgentDocument (to handle file uploads)
class AgentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDocument
        fields = ['id', 'document', 'uploaded_at']


# Serializer for Visitor
class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"


# Serializer for Chat
class ChatSerializer(serializers.ModelSerializer):
    Agent = AgentSerializer(read_only=True)
    visitor = VisitorSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = "__all__"


# Sales Techniques Serializer
class SalesTechniqueSerializor(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    documents = serializers.SerializerMethodField()
    
    class Meta:
        model = SalesTechnique
        fields = "__all__"
    
    def get_documents(self, obj):
        # Return all documents related to the agent
        documents = SalesTechniquesDocument.objects.filter(agent=obj)
        return SalesTechniquesDocumentSerializer(documents, many=True).data


class SalesTechniquesDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesTechniquesDocument
        fields = '__all__'


# Serializer to validate the email and password
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

