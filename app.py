import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Disability Resource Hub",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Better Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 1rem;
    }
    .section-header {
        color: #2c3e50;
        border-left: 4px solid #3498db;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    .task-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .priority-high { border-left: 4px solid #dc3545; }
    .priority-medium { border-left: 4px solid #ffc107; }
    .priority-low { border-left: 4px solid #28a745; }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown('<h1 class="main-header">🤝 Disability Resource & Project Management Hub</h1>', unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a section:",
    ["🏠 Dashboard", "📍 State Resources", "📋 Project Management", "📊 Analytics", "📚 Resource Library", "⚙️ Settings"]
)

# --- Initialize Session State ---
def init_session_state():
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "contacts" not in st.session_state:
        st.session_state.contacts = []
    if "appointments" not in st.session_state:
        st.session_state.appointments = []
    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "child_name": "",
            "child_age": "",
            "disabilities": [],
            "state": "California",
            "notifications": True
        }

init_session_state()

# --- Enhanced Resource Database ---
@st.cache_data
def load_comprehensive_resources():
    """Load a comprehensive database of disability resources by state"""
    resources_data = [
        # California Resources
        {"State": "California", "Category": "Healthcare", "Name": "California Children's Services", 
         "Link": "https://www.dhcs.ca.gov/services/ccs", "Phone": "(916) 552-9105", 
         "Description": "Provides diagnostic and treatment services, medical case management, and physical and occupational therapy services.",
         "Services": ["Medical Care", "Therapy", "Case Management"], "Ages": "0-21", "Cost": "Free/Low-cost"},
        
        {"State": "California", "Category": "Education", "Name": "Special Education Local Plan Area (SELPA)", 
         "Link": "https://www.cde.ca.gov/sp/se/lr/selpacontacts.asp", "Phone": "Varies by region",
         "Description": "Provides special education services and supports for students with disabilities.",
         "Services": ["IEP Development", "Special Education", "Related Services"], "Ages": "3-22", "Cost": "Free"},
        
        {"State": "California", "Category": "Support Services", "Name": "Regional Centers", 
         "Link": "https://www.dds.ca.gov/rc/", "Phone": "Varies by region",
         "Description": "Coordinate services for individuals with developmental disabilities and their families.",
         "Services": ["Service Coordination", "Respite Care", "Day Programs"], "Ages": "All ages", "Cost": "Varies"},
        
        {"State": "California", "Category": "Financial Support", "Name": "In-Home Supportive Services (IHSS)", 
         "Link": "https://www.cdss.ca.gov/in-home-supportive-services", "Phone": "(916) 651-5200",
         "Description": "Provides assistance with activities of daily living for eligible individuals.",
         "Services": ["Personal Care", "Domestic Services", "Protective Supervision"], "Ages": "All ages", "Cost": "Income-based"},
        
        # New York Resources
        {"State": "New York", "Category": "Healthcare", "Name": "Early Intervention Program", 
         "Link": "https://www.health.ny.gov/community/infants_children/early_intervention/", "Phone": "(518) 473-7016",
         "Description": "Services for infants and toddlers with disabilities or developmental delays.",
         "Services": ["Developmental Therapy", "Speech Therapy", "Occupational Therapy"], "Ages": "0-3", "Cost": "Insurance/Free"},
        
        {"State": "New York", "Category": "Education", "Name": "Committee on Special Education (CSE)", 
         "Link": "http://www.p12.nysed.gov/specialed/", "Phone": "(518) 474-2714",
         "Description": "Develops individualized education programs for students with disabilities.",
         "Services": ["IEP Development", "Special Education Placement", "Related Services"], "Ages": "3-21", "Cost": "Free"},
        
        {"State": "Texas", "Category": "Healthcare", "Name": "Early Childhood Intervention (ECI)", 
         "Link": "https://www.hhs.texas.gov/services/disability/early-childhood-intervention-eci", "Phone": "(512) 776-7000",
         "Description": "Services for children with disabilities or delays and their families.",
         "Services": ["Developmental Therapy", "Family Support", "Service Coordination"], "Ages": "0-3", "Cost": "Income-based"},
        
        {"State": "Florida", "Category": "Support Services", "Name": "Area Health Education Centers (AHEC)", 
         "Link": "https://ahectec.org/", "Phone": "(813) 974-4598",
         "Description": "Provides resources and support for families of children with special healthcare needs.",
         "Services": ["Information & Referral", "Family Support", "Education"], "Ages": "All ages", "Cost": "Free"},
        
        # Add more states...
        {"State": "Illinois", "Category": "Healthcare", "Name": "Division of Specialized Care for Children", 
         "Link": "https://dscc.uic.edu/", "Phone": "(217) 333-4224",
         "Description": "Provides care coordination and financial assistance for children with special healthcare needs.",
         "Services": ["Care Coordination", "Financial Assistance", "Family Support"], "Ages": "0-21", "Cost": "Income-based"}
    ]
    
    return pd.DataFrame(resources_data)

# --- Dashboard Page ---
if page == "🏠 Dashboard":
    st.markdown('<h2 class="section-header">Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([t for t in st.session_state.tasks if t["Status"] == "Completed"])
    overdue_tasks = len([t for t in st.session_state.tasks if t["Status"] != "Completed" and t["Deadline"] < datetime.now().date()])
    upcoming_tasks = len([t for t in st.session_state.tasks if t["Status"] != "Completed" and t["Deadline"] <= datetime.now().date() + timedelta(days=7)])
    
    with col1:
        st.metric("Total Tasks", total_tasks, delta=None)
    with col2:
        st.metric("Completed", completed_tasks, delta=f"{completed_tasks-total_tasks+completed_tasks if total_tasks > 0 else 0}")
    with col3:
        st.metric("Overdue", overdue_tasks, delta=None, delta_color="inverse")
    with col4:
        st.metric("Due This Week", upcoming_tasks, delta=None)
    
    # Quick Actions
    st.markdown('<h3 class="section-header">Quick Actions</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Add New Task", use_container_width=True):
            st.switch_page = "📋 Project Management"
    with col2:
        if st.button("📞 Add Contact", use_container_width=True):
            st.info("Contact management coming soon!")
    with col3:
        if st.button("📅 Schedule Appointment", use_container_width=True):
            st.info("Appointment scheduling coming soon!")
    
    # Recent Activity
    if st.session_state.tasks:
        st.markdown('<h3 class="section-header">Recent Tasks</h3>', unsafe_allow_html=True)
        recent_tasks = sorted(st.session_state.tasks, key=lambda x: x["Deadline"], reverse=True)[:5]
        for task in recent_tasks:
            status_color = {"Completed": "🟢", "In Progress": "🟡", "Not Started": "🔴"}
            st.write(f"{status_color.get(task['Status'], '⚪')} **{task['Task']}** - Due: {task['Deadline']} - Priority: {task.get('Priority', 'Medium')}")

# --- State Resources Page ---
elif page == "📍 State Resources":
    st.markdown('<h2 class="section-header">State-Specific Resources</h2>', unsafe_allow_html=True)
    
    # State Selection
    states = [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware",
        "Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
        "Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
        "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina",
        "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia",
        "Wisconsin","Wyoming"
    ]
    
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_state = st.selectbox("Select your state:", states, index=states.index(st.session_state.user_profile["state"]))
    with col2:
        category_filter = st.selectbox("Filter by category:", ["All", "Healthcare", "Education", "Support Services", "Financial Support"])
    
    # Load and filter resources
    resources_df = load_comprehensive_resources()
    state_resources = resources_df[resources_df['State'] == selected_state]
    
    if category_filter != "All":
        state_resources = state_resources[state_resources['Category'] == category_filter]
    
    if not state_resources.empty:
        st.success(f"Found {len(state_resources)} resources in {selected_state}")
        
        # Display resources in cards
        for idx, resource in state_resources.iterrows():
            with st.expander(f"🏢 {resource['Name']} - {resource['Category']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Description:** {resource['Description']}")
                    st.write(f"**Services:** {', '.join(eval(resource['Services']) if isinstance(resource['Services'], str) else resource['Services'])}")
                    st.write(f"**Ages Served:** {resource['Ages']}")
                    st.write(f"**Cost:** {resource['Cost']}")
                
                with col2:
                    st.write(f"**Phone:** {resource['Phone']}")
                    st.link_button("Visit Website", resource['Link'])
                    if st.button(f"Save to Contacts", key=f"save_{idx}"):
                        st.session_state.contacts.append({
                            "Name": resource['Name'],
                            "Phone": resource['Phone'],
                            "Website": resource['Link'],
                            "Category": resource['Category'],
                            "Notes": ""
                        })
                        st.success("Added to contacts!")
    else:
        st.info(f"No resources found for {selected_state} in the {category_filter} category. Please check back later as we're constantly updating our database.")
        
        # Suggest adding resources
        with st.expander("Know a resource we should add?"):
            with st.form("suggest_resource"):
                st.write("Help us expand our database!")
                name = st.text_input("Resource Name")
                category = st.selectbox("Category", ["Healthcare", "Education", "Support Services", "Financial Support"])
                description = st.text_area("Description")
                website = st.text_input("Website URL")
                phone = st.text_input("Phone Number")
                
                if st.form_submit_button("Suggest Resource"):
                    # In a real app, this would send the suggestion to a database
                    st.success("Thank you for your suggestion! We'll review it and add it to our database.")

# --- Project Management Page ---
elif page == "📋 Project Management":
    st.markdown('<h2 class="section-header">Project & Task Management</h2>', unsafe_allow_html=True)
    
    # Task input form
    with st.expander("➕ Add New Task", expanded=len(st.session_state.tasks) == 0):
        with st.form("enhanced_task_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                task_name = st.text_input("Task Name*")
                task_category = st.selectbox("Category", ["Therapy", "Education", "Healthcare", "Legal", "Financial", "Other"])
                task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                task_deadline = st.date_input("Deadline", datetime.today())
            
            with col2:
                task_description = st.text_area("Description (Optional)")
                assigned_to = st.text_input("Assigned To (Optional)")
                estimated_hours = st.number_input("Estimated Hours", min_value=0.5, max_value=100.0, value=1.0, step=0.5)
                reminder_days = st.selectbox("Remind me", [1, 3, 7, 14], format_func=lambda x: f"{x} day{'s' if x > 1 else ''} before")
            
            submitted = st.form_submit_button("Add Task", use_container_width=True)
            
            if submitted and task_name:
                new_task = {
                    "Task": task_name,
                    "Category": task_category,
                    "Priority": task_priority,
                    "Deadline": task_deadline,
                    "Status": "Not Started",
                    "Description": task_description,
                    "Assigned To": assigned_to or "Me",
                    "Estimated Hours": estimated_hours,
                    "Reminder Days": reminder_days,
                    "Created": datetime.now().date(),
                    "Progress": 0
                }
                st.session_state.tasks.append(new_task)
                st.success(f"Task '{task_name}' added successfully!")
                st.rerun()
    
    # Task management
    if st.session_state.tasks:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Not Started", "In Progress", "Completed"])
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
        with col3:
            category_filter = st.selectbox("Filter by Category", ["All", "Therapy", "Education", "Healthcare", "Legal", "Financial", "Other"])
        
        # Apply filters
        filtered_tasks = st.session_state.tasks.copy()
        if status_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t["Status"] == status_filter]
        if priority_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t["Priority"] == priority_filter]
        if category_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t["Category"] == category_filter]
        
        st.write(f"**Showing {len(filtered_tasks)} of {len(st.session_state.tasks)} tasks**")
        
        # Task cards
        for i, task in enumerate(st.session_state.tasks):
            if task in filtered_tasks:
                # Determine card styling based on priority
                priority_class = f"priority-{task['Priority'].lower()}"
                
                with st.container():
                    st.markdown(f'<div class="task-card {priority_class}">', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{task['Task']}**")
                        if task.get('Description'):
                            st.write(f"*{task['Description']}*")
                        st.write(f"📅 Due: {task['Deadline']} | 👤 {task['Assigned To']} | ⏱️ {task['Estimated Hours']}h")
                    
                    with col2:
                        new_status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"], 
                                                index=["Not Started", "In Progress", "Completed"].index(task["Status"]),
                                                key=f"status_{i}")
                        if new_status != task["Status"]:
                            st.session_state.tasks[i]["Status"] = new_status
                            st.rerun()
                    
                    with col3:
                        new_progress = st.slider("Progress", 0, 100, task.get("Progress", 0), key=f"progress_{i}")
                        if new_progress != task.get("Progress", 0):
                            st.session_state.tasks[i]["Progress"] = new_progress
                    
                    with col4:
                        if st.button("🗑️", key=f"delete_{i}", help="Delete task"):
                            st.session_state.tasks.pop(i)
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Export options
        st.markdown('<h3 class="section-header">Export Options</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Download as CSV"):
                tasks_df = pd.DataFrame(st.session_state.tasks)
                csv = tasks_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV file",
                    data=csv,
                    file_name=f"disability_tasks_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📊 Generate Report"):
                st.info("Detailed reporting available in Analytics section!")
    else:
        st.info("No tasks yet. Add your first task above to get started!")

# --- Analytics Page ---
elif page == "📊 Analytics":
    st.markdown('<h2 class="section-header">Analytics & Insights</h2>', unsafe_allow_html=True)
    
    if st.session_state.tasks:
        tasks_df = pd.DataFrame(st.session_state.tasks)
        
        # Task completion analytics
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution
            status_counts = tasks_df['Status'].value_counts()
            fig_pie = px.pie(values=status_counts.values, names=status_counts.index, 
                           title="Task Status Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Priority distribution
            priority_counts = tasks_df['Priority'].value_counts()
            fig_bar = px.bar(x=priority_counts.index, y=priority_counts.values,
                           title="Tasks by Priority Level")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Category breakdown
        category_counts = tasks_df['Category'].value_counts()
        fig_category = px.bar(x=category_counts.values, y=category_counts.index, 
                            orientation='h', title="Tasks by Category")
        st.plotly_chart(fig_category, use_container_width=True)
        
        # Progress tracking
        if 'Progress' in tasks_df.columns:
            avg_progress = tasks_df['Progress'].mean()
            st.metric("Average Task Progress", f"{avg_progress:.1f}%")
            
            # Progress over time (if we had date tracking)
            st.write("### Task Progress Overview")
            progress_data = tasks_df[['Task', 'Progress', 'Status']].copy()
            fig_progress = px.bar(progress_data, x='Task', y='Progress', 
                                color='Status', title="Individual Task Progress")
            fig_progress.update_xaxis(tickangle=45)
            st.plotly_chart(fig_progress, use_container_width=True)
        
        # Time management insights
        st.markdown('<h3 class="section-header">Time Management Insights</h3>', unsafe_allow_html=True)
        
        total_estimated_hours = tasks_df['Estimated Hours'].sum()
        completed_tasks = tasks_df[tasks_df['Status'] == 'Completed']
        completed_hours = completed_tasks['Estimated Hours'].sum() if not completed_tasks.empty else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Estimated Hours", f"{total_estimated_hours:.1f}")
        with col2:
            st.metric("Completed Hours", f"{completed_hours:.1f}")
        with col3:
            remaining_hours = total_estimated_hours - completed_hours
            st.metric("Remaining Hours", f"{remaining_hours:.1f}")
        
    else:
        st.info("No data available yet. Add some tasks to see analytics!")

# --- Resource Library Page ---
elif page == "📚 Resource Library":
    st.markdown('<h2 class="section-header">Resource Library</h2>', unsafe_allow_html=True)
    
    # Educational resources
    st.markdown("### 📖 Educational Resources")
    
    educational_resources = [
        {
            "title": "Understanding IEPs",
            "description": "A comprehensive guide to Individualized Education Programs",
            "type": "Guide",
            "url": "https://www.understood.org/en/school-learning/special-services/ieps/understanding-individualized-education-programs"
        },
        {
            "title": "Disability Rights in Education",
            "description": "Know your child's rights under IDEA and Section 504",
            "type": "Legal Info",
            "url": "https://www.parentcenterhub.org/repository/idea/"
        },
        {
            "title": "Transition Planning",
            "description": "Planning for life after high school",
            "type": "Planning Tool",
            "url": "https://www.transitionta.org/"
        }
    ]
    
    for resource in educational_resources:
        with st.expander(f"📚 {resource['title']} ({resource['type']})"):
            st.write(resource['description'])
            st.link_button("Access Resource", resource['url'])
    
    # Forms and templates
    st.markdown("### 📝 Forms & Templates")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**IEP Meeting Preparation Checklist**")
        st.download_button("Download Template", "IEP Meeting Checklist Template", "iep_checklist.txt")
    
    with col2:
        st.write("**Therapy Progress Tracker**")
        st.download_button("Download Template", "Therapy Progress Template", "therapy_tracker.txt")

# --- Settings Page ---
elif page == "⚙️ Settings":
    st.markdown('<h2 class="section-header">Settings & Profile</h2>', unsafe_allow_html=True)
    
    # User Profile
    with st.expander("👤 User Profile", expanded=True):
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                child_name = st.text_input("Child's Name", st.session_state.user_profile["child_name"])
                child_age = st.text_input("Child's Age", st.session_state.user_profile["child_age"])
                state = st.selectbox("State", states, index=states.index(st.session_state.user_profile["state"]))
            
            with col2:
                disabilities = st.multiselect("Disabilities/Conditions", 
                                           ["Autism", "ADHD", "Cerebral Palsy", "Down Syndrome", "Learning Disability", "Other"],
                                           st.session_state.user_profile["disabilities"])
                notifications = st.checkbox("Enable Notifications", st.session_state.user_profile["notifications"])
            
            if st.form_submit_button("Update Profile"):
                st.session_state.user_profile.update({
                    "child_name": child_name,
                    "child_age": child_age,
                    "disabilities": disabilities,
                    "state": state,
                    "notifications": notifications
                })
                st.success("Profile updated successfully!")
    
    # Data Management
    with st.expander("💾 Data Management"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Export All Data"):
                all_data = {
                    "tasks": st.session_state.tasks,
                    "contacts": st.session_state.contacts,
                    "profile": st.session_state.user_profile
                }
                st.download_button(
                    "Download Data",
                    json.dumps(all_data, default=str, indent=2),
                    file_name=f"disability_app_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🗑️ Clear All Data", type="secondary"):
                if st.button("⚠️ Confirm Delete All", type="primary"):
                    st.session_state.tasks = []
                    st.session_state.contacts = []
                    st.session_state.appointments = []
                    st.session_state.documents = []
                    st.success("All data cleared!")
                    st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>💙 Built with care for families navigating disability resources</p>
        <p>For support or feedback, contact: support@disabilityresourcehub.org</p>
    </div>
    """, 
    unsafe_allow_html=True
)
