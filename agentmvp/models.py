from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """
    Custom validator to ensure only .docx and .pdf files are uploaded.
    """
    allowed_extensions = ['.docx', '.pdf']
    if not any(value.name.endswith(ext) for ext in allowed_extensions):
        raise ValidationError(
            _(f'Invalid file type: {value.name}. Only .docx and .pdf files are allowed.')
        )

# Model for Customer (User)
class Customer(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]

    firstName = models.CharField(max_length=50, blank=False)
    lastName = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    password = models.CharField(max_length=255, blank=False)  # Store hashed passwords
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number field
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return (
            f"id: {self.id}, firstName: {self.firstName}, lastName: {self.lastName}, "
            f"email: {self.email}, phone_number: {self.phone_number}, role: {self.role}"
        )


# Model for Agent
class Agent(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='chatbots')
    name = models.CharField(max_length=255, blank=True, null=True)  # Optional name for the Agent
    website_url = models.URLField(max_length=255)  # Stores a URL
    date_scrap_time = models.DateTimeField(auto_now_add=True)  # Automatically sets the time when a record is created
    business_information = models.TextField()  # Stores a large block of text (e.g., business details)
    logo = models.FileField(
        upload_to='Agents_logo/',
        blank=True,
        null=True,
    )  
    class Meta:
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['website_url']),
        ]

    def __str__(self):
        # Truncate business_information for readability
        business_info_preview = self.business_information[:50] + '...' if len(self.business_information) > 50 else self.business_information
        return f"id: {self.id}, Customer: {self.customer.firstName} {self.customer.lastName}, Website: {self.website_url}, Scrap Time: {self.date_scrap_time}, Business Info: {business_info_preview}, Logo {self.logo}"

# New model for storing multiple documents per agent
class AgentDocument(models.Model):
    agent = models.ForeignKey(Agent, related_name='documents', on_delete=models.CASCADE)  # Link to the agent
    document = models.FileField(upload_to='business_docs/', validators=[validate_file_extension])  # File field for documents
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the document is uploaded

    def __str__(self):
        return f"Document {self.document.name} for Agent {self.agent.name}"




# Model for Visitor
class Visitor(models.Model):
    uuid = models.UUIDField(unique=True, default=models.UUIDField)  # Ensure the UUID is automatically generated
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation time
    updated_at = models.DateTimeField(auto_now=True)  # Track last updated time

    def __str__(self):
        return f"id: {self.id}, UUID: {self.uuid}"

# Model for Chat
class Chat(models.Model):
    ROLE_CHOICES = [
        ('visitor', 'Visitor'),
        ('agent', 'Agent'),
    ]
    Agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='chats')
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='chats')
    chat_content = models.TextField(max_length=500)  # Limit content to 500 characters
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # Track the time chat was created
    updated_at = models.DateTimeField(auto_now=True)  # Track last update time

    def __str__(self):
        # Preview of chat content for readability
        preview_content = self.chat_content[:50] + '...' if len(self.chat_content) > 50 else self.chat_content
        return f"Chat ID: {self.id}, Agent: {self.Agent.id}, Visitor: {self.visitor.uuid}, Role: {self.role}, Content: {preview_content}, Created At: {self.created_at}"






# sales techniques Model
class SalesTechnique(models.Model):
    STATUS_CHOICES = [
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    ]

    agent = models.ForeignKey(
        'Agent',
        on_delete=models.CASCADE,
        related_name='sales_techniques',
    )
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    information = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='disabled',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Technique: {self.name}, Status: {self.status}, Agent: {self.agent.id}, Description : {self.description}, Information : {self.information}"
    





class SalesTechniquesDocument(models.Model):
    salesTechnique = models.ForeignKey(SalesTechnique, related_name='documents', on_delete=models.CASCADE)  # Link to the SalesTechnique
    document = models.FileField(upload_to='sales_techniques_docs/')  # File field for documents
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the document is uploaded

    def __str__(self):
        # Correct the string representation to access the related SalesTechnique
        return f"Document {self.document.name} for SalesTechnique {self.salesTechnique.name}"
