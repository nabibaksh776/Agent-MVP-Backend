import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Agent, Visitor,SalesTechnique,Chat,AgentDocument,SalesTechniquesDocument
from .serializers import CustomerSerializer,AgentSerializer,VisitorSerializer,SalesTechniqueSerializor,ChatSerializer
from django.contrib.auth.hashers import make_password, check_password
from .utils import JWTAuthentication, generate_jwt_tokens,validate_file_extension
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser


# handle current user

class HandleCurrentUser(APIView):

    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            currentUser = request.user
            customerSrializer = CustomerSerializer(currentUser)
            return Response(
                {"data": customerSrializer.data},status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message" : "no current user found"}, status=status.HTTP_404_NOT_FOUND
            )
# CreateCustomer view using Django REST Framework
# ###############################
# 
# 
#  FUNCTION TO Create/Register Customer
# 
# 
# ###############################
class HANDLE_CUSTOMER(APIView):
    """
    Handles GET and POST requests for creating and retrieving customers.
    """
    authentication_classes = [JWTAuthentication]
    def get(self, request, customer_id=None):
        """
        Fetch a specific customer by ID or all customers if no ID is provided.
        """
        if customer_id:  # If a customer_id is provided, fetch a specific customer by ID
            try:
                customer = Customer.objects.get(id=customer_id)
                serializer = CustomerSerializer(customer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Customer.DoesNotExist:
                return Response({"status": 404, "message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        else:  # If no customer_id is provided, get all customers
            customers = Customer.objects.filter(role="customer")
            serializer = CustomerSerializer(customers, many=True)
            return Response(
                {
                "data":serializer.data
                }, status=status.HTTP_200_OK)
    
    
    

    def delete(self, request, customer_id=None):
        """
        Deletes a specific customer by ID.
        """
        currentUser = request.user
        if hasattr(currentUser, 'role') and currentUser.role == 'customer':
            return Response({"message": "Admin user accessed this endpoint."}, status=status.HTTP_400_BAD_REQUEST)
        

        if not customer_id:
            return Response(
                {"status": 400, "message": "Customer ID is required to delete a customer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the customer by ID
            customer = Customer.objects.get(id=customer_id)
            # Delete the customer
            customer.delete()


            customers = Customer.objects.filter(role="customer")
            serializer = CustomerSerializer(customers, many=True)
            return Response(
                {
                "data" : serializer.data,
                "status": 200, 
                 "message": f"Customer with ID {customer_id} deleted successfully."
                 },
                status=status.HTTP_200_OK
            )
        except Customer.DoesNotExist:
            return Response(
                {"status": 404, "message": "Customer not found."},
                status=status.HTTP_404_NOT_FOUND
            )


# admin update customer
class UpdteCustomer(APIView):
        # function to update customer
    authentication_classes = [JWTAuthentication]
    def patch(self,request,customer_id=None):

        currentUser = request.user
        if hasattr(currentUser, 'role') and currentUser.role == 'customer':
            return Response({"message": "Admin user accessed this endpoint."}, status=status.HTTP_400_BAD_REQUEST)
        

        if customer_id:
            data = request.data
            try:
                customer = Customer.objects.get(id=customer_id)
                if customer:
                    if "firstName" in data:
                        customer.firstName = data["firstName"]
                    if "lastName" in data:
                        customer.lastName = data["lastName"]
                    if "email" in data:
                        customer.email = data["email"]
                    if "phone_number" in data:
                        customer.phone_number = data["phone_number"]

                    customer.save() 
                    customers = Customer.objects.filter(role="customer")
                    serializer = CustomerSerializer(customers, many=True)
                    return Response({
                    "data" : serializer.data,
                    "message":"customer updated successfully"
                    },
                    status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            "message" : "invalid customer"
                        }, status=status.HTTP_400_BAD_REQUEST
                    )

            except Customer.DoesNotExist:
                return Response(
                    {"message" : "No customer found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        else:
            return Response(
                {"message" : "customer_id required"}, status=status.HTTP_400_BAD_REQUEST
            )

# ###############################
# 
# 
#  FUNCTION TO Login, Register customer
# 
# 
# ###############################
class CreateCustomer(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
            
            currentUser = request.user
            if hasattr(currentUser, 'role') and currentUser.role == 'customer':
                print("The current user is an admin!")  # Print to console
                return Response({"message": "Admin user accessed this endpoint."}, status=status.HTTP_400_BAD_REQUEST)
            
            print("user is---", currentUser)
            data = request.data
            firstName = data.get('firstName')
            lastName = data.get('lastName')
            email = data.get('email')
            phone_number = data.get('phone_number')
            # Required fields validation
            required_fields = ["firstName", "lastName", "email", "password"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return Response(
                    {"status": 400, "message": f"Missing required fields: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                hashed_password = make_password(data.get("password"))
                print("password is---", hashed_password)
                try:
                    findCustomer = Customer.objects.get(email=email)
                    return Response(
                        {"message":"email already exist"}
                        ,status=status.HTTP_400_BAD_REQUEST
                        )
                except Customer.DoesNotExist:
                    Customer.objects.create(
                        firstName=firstName,
                        lastName=lastName,
                        email=email,
                        password=hashed_password,  # Store the hashed password
                        phone_number=phone_number,
                        role="customer",
                    )


                    customers = Customer.objects.filter(role="customer")
                    serializer = CustomerSerializer(customers, many=True)
                    return Response(
                        {"data" : serializer.data}, status=status.HTTP_200_OK
                    )
            except Exception as e:
                print("e--",e)
                return Response(
                    {"message":"customer not created"},
                    status=status.HTTP_400_BAD_REQUEST
                )




# function to login the user/Admin
class LoginCustomer(APIView):
    """
    View for customer login.
    """

    def get(self, request):
        """
        Handle GET request only with a message.
        """
        return Response(
            {"message": "Only POST method is allowed for login"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request):
        """
        Handle POST login logic.
        """
        try:
            # Extract data from the request payload
            data = request.data
            email = data.get("email")
            password = data.get("password")

            # Validate presence of email & password
            if not email or not password:
                print("Email or password is missing in request.")
                return Response(
                    {"message": "Email or password required"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Attempt to find customer by email
            try:
                customer = Customer.objects.get(email=email)
                print("Customer found:", customer)

                # Validate the password
                if not check_password(password, customer.password):
                    print("Password does not match.")
                    return Response(
                        {"message": "Invalid email or password"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                
            except Customer.DoesNotExist:
                # Handle the case where no customer is found with this email
                print("No customer found with that email.")
                return Response(
                    {"message": "Invalid email or password"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Generate JWT tokens
            tokens = generate_jwt_tokens(customer)
            # Serialize customer data
            customer_serializer = CustomerSerializer(customer)
            # Respond with token and customer data
            return Response(
                {
                    "token": tokens,
                    "data": customer_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Log the unexpected exception
            print("Unexpected error during login:", e)
            return Response(
                {"message": "An internal server error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        






# ###############################
# 
# 
#  FUNCTION TO CREATE AGENTS 
# 
# 
# ###############################

class CREATE_AGENTS(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, agent_id=None):        
        if agent_id:
            try:
                agents = Agent.objects.select_related("customer").get(id=agent_id)
                serializer_agent = AgentSerializer(agents)
                return Response(serializer_agent.data, status=status.HTTP_200_OK)
            except Agent.DoesNotExist:
                return Response({"message": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            agents = Agent.objects.all()
            print("all agents--", agents)
            serializer_agent = AgentSerializer(agents, many=True)
            # return Response(serializer_agent.data, status=status.HTTP_200_OK)
            return Response(serializer_agent.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        customer = request.user
        print("user id---",customer.id)
        # Extract the data and uploaded file
        data = request.data
        name = data.get("name")
        website_url = data.get("website_url")
        business_information = data.get("business_information")
        business_docx = request.FILES.get("business_docx")  # Uploaded file

        print("document is--", business_docx)
        # Validate required fields
        if not name:
            return Response(
                {"message": "name is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not website_url:
            return Response(
                {"message": "website_url is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not business_information:
            return Response(
                {"message": "business_information is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not business_docx:
            return Response(
                {"message": "business_docx file is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate uploaded file extension
        if not validate_file_extension(business_docx):
            return Response(
                {"message": "Invalid file type. Only .docx or .pdf files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Attempt to find the customer from the database
        try:
            customer = Customer.objects.get(id=customer.id)
        except Customer.DoesNotExist:
            return Response(
                {"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Create the Agent instance
        agent = Agent.objects.create(
            customer=customer,
            name=name,
            website_url=website_url,
            business_information=business_information,
            business_docx=business_docx,
        )

        # Save the data to the database
        agent.save()

        return Response(
            {"message": "Agent created successfully."},
            status=status.HTTP_201_CREATED,
        )

    # function to delete
    def delete(self,request,agent_id=None):

        if agent_id:
            agent = Agent.objects.get(id=agent_id)
            # Delete the customer
            print("agent is-", agent)
            agent.delete()
            return Response(
                {"message":"agent deleted seccessfully"},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"message" :"no agent_id found"}, status=status.HTTP_400_BAD_REQUEST)
        

    # function to update agent








# ###############################
# 
# 
#  FUNCTION TO CREATE Visitor 
# 
# 
# ###############################

class VISITOR_VIEW_CLASS(APIView):
    
    def get(self,request,visitor_id=None):
        
        if visitor_id:
            try:
            
                visitor = Visitor.objects.get(id=visitor_id)
                visitor_serilizer = VisitorSerializer(visitor)
                return Response({"data" : visitor_serilizer.data}, status=status.HTTP_200_OK)
            except Visitor.DoesNotExist:
                return Response({"data": []}, status=status.HTTP_400_BAD_REQUEST)
        else:
            visitors = Visitor.objects.all()
            print("all visitors--", visitors)
            visitor_serilizer = VisitorSerializer(visitors, many=True)
            return Response({"data" : visitor_serilizer.data}, status=status.HTTP_200_OK)


    def post(self,request):
        data = request.data
        uuid = data.get("uuid")
        
        if not uuid:
            return Response({"message" : "uuid required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_visitor = Visitor.objects.create(
                uuid=uuid
            )
        except Exception as e:
            return Response({"message" : "invalid uuid"}, status=status.HTTP_400_BAD_REQUEST)

        new_visitor.save()
        return Response({"message" : "new visitor added"}, status= status.HTTP_200_OK)
    

    # function to delete visitor
    def delete(self,request,visitor_id=None):
        if visitor_id:
            try:
                visitors = Visitor.objects.get(id=visitor_id)
                # Delete the customer
                print("agent is-", visitors)
                visitors.delete()
                return Response({"message" : "visitor deleted successfully"}, status=status.HTTP_200_OK)
            except Visitor.DoesNotExist:
                return Response({"message" : "not visitor found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message" : "visitor_id requied"})





# ###############################
# 
# 
#  FUNCTION TO Add, Update,Get, Delete Sales Techniques
# 
# 
# ###############################
class SALES_TECHNIQUES(APIView):
    authentication_classes = [JWTAuthentication]



    def get(self, request,technique_id=None):

        if technique_id:
            
            try:
                techniques = SalesTechnique.objects.get(id=technique_id)
                serilizedTechniques = SalesTechniqueSerializor(techniques)
                return Response({
                    "data":serilizedTechniques.data
                }, status=status.HTTP_200_OK)
            
            except SalesTechnique.DoesNotExist:
                return Response(
                    {
                        "data" : []
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        else:
            techniques = SalesTechnique.objects.all()
            serilizedTechniques = SalesTechniqueSerializor(techniques, many=True)
            return Response({
               "data":serilizedTechniques.data
            },status=status.HTTP_200_OK)

    # create sales techniques
    def post(self, request):
        customer = request.user
        data = request.data
        name = data.get("name")
        description = data.get("description")
        information = data.get("information")
        document = request.FILES.get("document")
        agent_id = data.get("agent_id")

        required_fields = ["name", "description", "information", "document","agent_id"]

        missing_fields = [field for field in required_fields if not data.get(field) and field != "document"]
        
        if "document" not in request.FILES:
            missing_fields.append("document")

        if missing_fields:
            return Response(
                {"message": f"The following fields are required: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        


        try:
            customer = Customer.objects.get(id=customer.id)
        except Customer.DoesNotExist:
            return Response(
                {"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND
            )
        

        try:
            agent = Agent.objects.get(id =agent_id)
        except Agent.DoesNotExist:
            return Response(
                {"message" : "Agent not found"},status=status.HTTP_400_BAD_REQUEST
            )


        S_techniques = SalesTechnique.objects.create(
            agent=agent,
            document=document,
            name=name,
            description=description,
            information=information,
        )

        S_techniques.save()  
        # Proceed with your logic here
        return Response({"message": "new technique added successfully"}, status=status.HTTP_200_OK)
    



    # upate sales Techniques
    def patch(self,request,technique_id=None):

        if technique_id:
            data = request.data
            try:
                s_technique = SalesTechnique.objects.get(id=technique_id)
                print("this is tech--", s_technique)
            except SalesTechnique.DoesNotExist:
                return Response(
                    {
                        "message" : "No Sales Technique found"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )   
            
            if "name" in data:
                s_technique.name = data["name"]
            if "description" in data:
                s_technique.description = data["description"]
            if "information" in data:
                s_technique.information = data["information"]
            if "status" in data:
                s_technique.status = data["status"]
            if "document" in request.FILES:
                s_technique.document = request.FILES["document"]
            
            s_technique.save()
            return Response(
                {"message" : "sales Techniques updated successfully"},
                status=status.HTTP_200_OK
            )
        
        else:
            return Response({
                "message" : "technique_id requied"
            }, status=status.HTTP_400_BAD_REQUEST)
        


    # function to delete technique
    def delete(self,request,technique_id=None):

        if not technique_id:
            return Response(
                {"message" : "technique_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        technique = SalesTechnique.objects.get(id=technique_id)
        technique.delete()
        return Response(
            {
                "message" : "Sales Technique has been deleted"
            },
            status=status.HTTP_200_OK
        )

    





# ###############################
# 
# 
#  FUNCTION TO Add, Update,Get, Delete Chat
# 
# 
# ###############################
class CHAT_CLASS(APIView):
    authentication_classes = [JWTAuthentication]

    # function to delete chat by id
    def delete(self,request, chat_id=None):
        if chat_id:
            try:
                chat_data = Chat.objects.get(id=chat_id)
                chat_data.delete()
                return Response(
                    {
                        "message" : "chat deleted successfully"
                    },
                    status=status.HTTP_200_OK
                )
            except Chat.DoesNotExist:
                return Response(
                    {
                        "message" : "chat not found"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message" : "chat_id required"},status=status.HTTP_400_BAD_REQUEST
            )
            
    # function to get single chat, all chat
    def get(self,request, chat_id=None):
        
        if chat_id:
            try:
                chat_data = Chat.objects.get(id=chat_id)
                chatSerializerData = ChatSerializer(chat_data)
                return Response({
                    "data":chatSerializerData.data
                }, status=status.HTTP_200_OK)
            except Chat.DoesNotExist:
                return Response(
                    {"data" : []},status=status.HTTP_400_BAD_REQUEST
                )
        else:
            try:
                chat_data = Chat.objects.all()
                chatSerializerData = ChatSerializer(chat_data, many=True)
                return Response({
                    "data":chatSerializerData.data
                }, status=status.HTTP_200_OK)
            except Chat.DoesNotExist:
                return Response(
                    {"data" : []},status=status.HTTP_400_BAD_REQUEST
                )




    # post chat
    def post(self,request):

        data = request.data 
        agent_id = data.get("agent_id")
        visitor_id = data.get("visitor_id")
        chat_content = data.get("chat_content")
        role = data.get("role") # visitor, agent

        required_fields = ["agent_id", "visitor_id", "chat_content", "role"]

        missing_fields = [field for field in required_fields if not data.get(field)]
        

        if role != "visitor" and role != "agent":
            return Response(
                {
                    "message" : "role should be agent or visitor required"
                },status=status.HTTP_400_BAD_REQUEST
            )

        if missing_fields:
            return Response(
                {"message": f"The following fields are required: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
            

        try:
            agent = Agent.objects.get(id=agent_id)
        except Agent.DoesNotExist:
            return Response(
                {
                    "message":"agent does not exist"
                },status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            visitor = Visitor.objects.get(id=visitor_id)
        except Visitor.DoesNotExist:
            return Response(
                {
                    "message":"visitor does not exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        new_chat = Chat.objects.create(
            Agent = agent,
            visitor=visitor,
            chat_content=chat_content,
            role=role,
        )
                
        new_chat.save()
        return Response(
            {
                "message" : "message sent successfully"
            },status=status.HTTP_200_OK
        )







# ###############################
# 
# 
#  admin routes
# 
# 
# ###############################
class ADMIN_MANAGE(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            
            admin = Customer.objects.filter(role="admin")
            adminSerializer = CustomerSerializer(admin, many=True)

            return Response(
                {
                "data": adminSerializer.data
                }, status=status.HTTP_200_OK
            )
        except Customer.DoesNotExist:
            return Response({
                "message" : "admin not found"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        
        
    # function to delete chat by id
    def patch(self,request, admin_id=None):
        data = request.data
        if admin_id:
            try:
                admin = Customer.objects.get(id=admin_id, role="admin")

                if "firstName" in data:
                    admin.firstName = data["firstName"]
                if "lastName" in data:
                    admin.lastName = data["lastName"]
                if "email" in data:
                    admin.email = data["email"]
                if "phone_number" in data:
                    admin.phone_number = data["phone_number"]


                admin.save()
                return Response(
                    {"message" : "admin update successfully"}
                ,status=status.HTTP_200_OK)
            except Customer.DoesNotExist:
                return Response(
                    {"message" : "admin not found"}
                ,status=status.HTTP_200_OK)
            
        else:
            return Response(
                {"message" : "admin_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )







# 
# 
# Logout View
# 
# 

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            print("this si token ---", token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("e---",e)
            return Response({"error": "Invalid refresh token or logout failed"}, status=status.HTTP_400_BAD_REQUEST)
        




# 
# 
# GET Agents by Customer ID
# 
# 
class AdminManageAgents(APIView):
    authentication_classes = [JWTAuthentication]


    def get(self, request, customer_id:None):
        currentUser = request.user
        if hasattr(currentUser, 'role') and currentUser.role == 'customer':
            return Response({"message": "Admin user accessed this endpoint."}, status=status.HTTP_400_BAD_REQUEST)

        if customer_id:
            try:
                agents = Agent.objects.filter(customer=customer_id)
                print("agents---", agents)
                serializer = AgentSerializer(agents, many=True)
                return Response(
                    {
                    "data":serializer.data
                    }, status=status.HTTP_200_OK)
            except Agent.DoesNotExist:
                 return Response(
                {
                "data":"agents not found"
                }, status=status.HTTP_400_BAD_REQUEST)


        else:
            agents = Agent.objects.all()
            serializer = AgentSerializer(agents, many=True)
            return Response(
                {
                "data":serializer.data
                }, status=status.HTTP_200_OK)
    
    
    parser_classes = (MultiPartParser,)
    def post(self, request):
        currentUser = request.user
        if hasattr(currentUser, 'role') and currentUser.role == 'customer':
            return Response({"message": "Admin user accessed this endpoint."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the data
        data = request.data
        print('data is--', data)
        name = data.get("name")
        website_url = data.get("website_url")
        business_information = data.get("business_information")
        customer_id = data.get("customer_id")
        business_docx_files = request.FILES.getlist("business_docx_files")  # Multiple files
        logo_file = request.FILES.get("logo_file")  # Single file for the logo

        # sales technique data
        Sales_techniques_files = request.FILES.getlist("Sales_techniques_files")  # sales Techniques files
        TName = data.get("TName")  # sales Techniques files
        TDescription = data.get("TDescription")  # sales Techniques files
        Tinformation = data.get("Tinformation")   # sales Techniques files

        # Validate required fields
        if not customer_id:
            return Response({"message": "customer_id required"}, status=status.HTTP_400_BAD_REQUEST)
        if not name:
            return Response({"message": "name is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not website_url:
            return Response({"message": "website_url is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not business_information:
            return Response({"message": "business_information is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not business_docx_files:
            return Response({"message": "At least one business_docx file is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file extensions for business_docx_files (if needed)
        for file in business_docx_files:
            if not validate_file_extension(file):
                return Response({"message": "Invalid file type. Only .docx or .pdf files are allowed."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate logo file (only .jpg, .jpeg, .png files are allowed)
        if logo_file:
            if not logo_file.name.lower().endswith(('jpg', 'jpeg', 'png')):
                return Response({"message": "Invalid logo file type. Only .jpg, .jpeg, .png files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Find the customer
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the Agent instance
        agent = Agent.objects.create(
            customer=customer,
            name=name,
            website_url=website_url,
            business_information=business_information,
            logo=logo_file if logo_file else None,  # Save the logo if uploaded
        )

        # Save the documents for the agent
        for file in business_docx_files:
            AgentDocument.objects.create(agent=agent, document=file)

        
        if TName and TDescription and Tinformation:
            s_techNique = SalesTechnique.objects.create(
                agent=agent,
                name=TName,
                description=TDescription,
                information=Tinformation,
            )
            
            # save sales technique file
            if Sales_techniques_files:
                for file in Sales_techniques_files:
                    SalesTechniquesDocument.objects.create(salesTechnique=s_techNique, document=file)

            


        

        return Response({"message": "Agent and documents created successfully."}, status=status.HTTP_201_CREATED)
    





class UpdateAgentByAdmin(APIView):

       # update agents
    authentication_classes = [JWTAuthentication]
    def patch(self, request, agent_id=None):
        current_user = request.user

        # Permission Check
        if hasattr(current_user, 'role') and current_user.role == 'customer':
            return Response({"message": "You do not have permission to update agents."}, status=status.HTTP_403_FORBIDDEN)

        # Ensure agent_id is provided
        if not agent_id:
            return Response({"message": "Agent ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the agent
        try:
            agent = Agent.objects.get(id=agent_id)
        except Agent.DoesNotExist:
            return Response({"message": "Agent not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update agent's information
        try:
            data = request.data
            print("Received data for patch:", data)

            # Update fields
            if "name" in data:
                agent.name = data["name"]
            if "website_url" in data:
                agent.website_url = data["website_url"]
            if "business_information" in data:
                agent.business_information = data["business_information"]

            # Handle logo update if the logo file is provided in the payload
            logo_file = request.FILES.get("logo_file")  # Extract the logo file from the request
            if logo_file:
                # Check and delete the old logo if it exists
                if agent.logo:
                    # Delete the old logo file from the filesystem
                    if os.path.isfile(agent.logo.path):
                        os.remove(agent.logo.path)
                
                # Validate logo file extension
                if not logo_file.name.lower().endswith(('jpg', 'jpeg', 'png')):
                    return Response({"message": "Invalid logo file type. Only .jpg, .jpeg, .png files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

                # Save the new logo for the agent
                agent.logo = logo_file

            # Save the agent after making the changes
            agent.save()

            # Retrieve the updated agent data
            updated_agent = Agent.objects.get(id=agent_id)
            updated_agent_serializer = AgentSerializer(updated_agent)

            return Response(
                {
                    "message": "Agent updated successfully.",
                    "data": updated_agent_serializer.data
                }, status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"Error while updating agent: {e}")
            return Response({"message": "Failed to update the agent."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# delete agent by id
    def delete(self, request, agent_id=None):
            current_user = request.user

            # Permission Check
            if hasattr(current_user, 'role') and current_user.role == 'customer':
                return Response({"message": "You do not have permission to delete agents."}, status=status.HTTP_403_FORBIDDEN)

            # Ensure agent_id is provided
            if not agent_id:
                return Response({"message": "Agent ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the agent
            try:
                agent = Agent.objects.get(id=agent_id)
            except Agent.DoesNotExist:
                return Response({"message": "Agent not found."}, status=status.HTTP_404_NOT_FOUND)

            # Delete the old logo if it exists
            if agent.logo:
                try:
                    # Check if the logo exists and delete it from the filesystem
                    if os.path.isfile(agent.logo.path):
                        os.remove(agent.logo.path)
                except Exception as e:
                    print(f"Error while deleting logo: {e}")

            # Delete the agent
            agent.delete()

            # Return response indicating deletion success
            return Response({"message": "Agent deleted successfully."}, status=status.HTTP_200_OK)
        







# ManageAgentDocx document
class ManageAgentDocx(APIView):

    authentication_classes = [JWTAuthentication]
    def delete(self, request, doc_id=None):
        current_user = request.user

            # Permission Check
        if hasattr(current_user, 'role') and current_user.role == 'customer':
            return Response({"message": "only admin can access the route."}, status=status.HTTP_403_FORBIDDEN)
        

        try:
            if doc_id:
                document = AgentDocument.objects.get(id=doc_id)
                
                # Delete the file from the file system
                if document.document:
                    document.document.delete(save=False)  # Deletes file from storage
                
                # Delete the instance from the database
                document.delete()
                
                return Response({"message": "Document deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "doc_id required"}, status=status.HTTP_400_BAD_REQUEST)
        except AgentDocument.DoesNotExist:
            return Response({"message": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    # upload file
    def post(self, request):
        current_user = request.user
        
        # Permission Check
        if hasattr(current_user, 'role') and current_user.role == 'customer':
            return Response({"message": "Only admin can access this route."}, status=status.HTTP_403_FORBIDDEN)
        
        agent_id = request.data.get('agent_id')
        file = request.FILES.get('document')

        if not agent_id:
            return Response({"message": "agent_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not file:
            return Response({"message": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the file type
        allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if file.content_type not in allowed_types:
            return Response({"message": "Only .docx and .pdf files are allowed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agent = Agent.objects.get(id=agent_id)

            # Create a new document record
            document = AgentDocument.objects.create(
                agent=agent,
                document=file
            )

            return Response({
                "message": "File uploaded successfully",
                "data": {
                    "id": document.id,
                    "document": document.document.name,
                    "uploaded_at": document.uploaded_at
                }
            }, status=status.HTTP_201_CREATED)
        except Agent.DoesNotExist:
            return Response({"message": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    











