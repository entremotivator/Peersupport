import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import json
import time

# Page configuration
st.set_page_config(
    page_title="Special Needs Parenting Support Hub",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .section-header {
        font-size: 1.8rem;
        color: #A23B72;
        margin-bottom: 1rem;
        border-bottom: 2px solid #F18F01;
        padding-bottom: 0.5rem;
    }
    
    .emergency-card {
        background-color: #ffebee;
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .milestone-card {
        background-color: #f3e5f5;
        border: 1px solid #9c27b0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .resource-card {
        background-color: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    .stButton > button {
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

if "emergency_contacts" not in st.session_state:
    st.session_state.emergency_contacts = []

if "milestone_shares" not in st.session_state:
    st.session_state.milestone_shares = []

if "crisis_plans" not in st.session_state:
    st.session_state.crisis_plans = []

if "saved_resources" not in st.session_state:
    st.session_state.saved_resources = []

# Sidebar navigation
st.sidebar.markdown("# 🌟 Navigation")
selected_page = st.sidebar.selectbox(
    "Choose a section:",
    [
        "🏠 Home Dashboard",
        "👤 User Profile", 
        "🎉 Milestone Tracking",
        "📱 Crisis Support",
        "📚 Resources & Forms",
        "📊 Progress Analytics"
    ]
)

# Main header
st.markdown('<h1 class="main-header">🌟 Special Needs Parenting Support Hub</h1>', unsafe_allow_html=True)

# --- Home Dashboard ---
if selected_page == "🏠 Home Dashboard":
    st.markdown('<h2 class="section-header">🏠 Welcome to Your Support Hub</h2>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        milestone_count = len(st.session_state.milestone_shares)
        st.metric("🎉 Milestones Shared", milestone_count)
    
    with col2:
        emergency_contacts_count = len(st.session_state.emergency_contacts)
        st.metric("📞 Emergency Contacts", emergency_contacts_count)
    
    with col3:
        crisis_plans_count = len(st.session_state.crisis_plans)
        st.metric("📋 Crisis Plans", crisis_plans_count)
    
    with col4:
        saved_resources_count = len(st.session_state.saved_resources)
        st.metric("📚 Saved Resources", saved_resources_count)
    
    # Quick access buttons
    st.markdown("### 🚀 Quick Access")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚨 Emergency Resources", use_container_width=True, type="primary"):
            st.session_state.selected_page = "📱 Crisis Support"
            st.rerun()
    
    with col2:
        if st.button("🎉 Share a Milestone", use_container_width=True):
            st.session_state.selected_page = "🎉 Milestone Tracking"
            st.rerun()
    
    with col3:
        if st.button("📚 Browse Resources", use_container_width=True):
            st.session_state.selected_page = "📚 Resources & Forms"
            st.rerun()
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    
    if st.session_state.milestone_shares:
        recent_milestones = sorted(st.session_state.milestone_shares, key=lambda x: x["date"], reverse=True)[:3]
        st.markdown("**🎉 Recent Milestones:**")
        for milestone in recent_milestones:
            st.write(f"• {milestone['text']} ({milestone['date']})")
    else:
        st.info("No recent milestones. Share your first milestone to get started!")
    
    # Daily tip
    tips = [
        "Remember to celebrate small victories - every step forward matters! 🌟",
        "Take time for self-care today. You can't pour from an empty cup. ☕",
        "Connect with other parents in your community for support and friendship. 👥",
        "Document your child's progress - it helps you see how far you've come! 📝",
        "Trust your instincts as a parent. You know your child best. 💝"
    ]
    
    import random
    daily_tip = random.choice(tips)
    st.markdown(f"### 💡 Daily Tip")
    st.info(daily_tip)

# --- User Profile Page ---
elif selected_page == "👤 User Profile":
    st.markdown('<h2 class="section-header">👤 User Profile</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👨‍👩‍👧‍👦 Family Info", "⚙️ Preferences", "📊 Account Stats"])
    
    with tab1:
        st.markdown("### 👨‍👩‍👧‍👦 Family Information")
        
        with st.form("family_profile"):
            col1, col2 = st.columns(2)
            
            with col1:
                parent_name = st.text_input("Parent/Guardian Name", 
                    value=st.session_state.user_profile.get("parent_name", ""))
                family_size = st.number_input("Family Size", min_value=1, max_value=20, 
                    value=st.session_state.user_profile.get("family_size", 1))
                location = st.text_input("Location (City, State)", 
                    value=st.session_state.user_profile.get("location", ""))
            
            with col2:
                primary_language = st.selectbox("Primary Language", 
                    ["English", "Spanish", "French", "German", "Other"],
                    index=0 if not st.session_state.user_profile.get("primary_language") else 
                    ["English", "Spanish", "French", "German", "Other"].index(st.session_state.user_profile.get("primary_language", "English")))
                support_network = st.multiselect("Support Network", 
                    ["Extended Family", "Friends", "Neighbors", "Support Groups", "Therapists", "Teachers", "Medical Team"],
                    default=st.session_state.user_profile.get("support_network", []))
            
            # Children information
            st.markdown("#### 👶 Children Information")
            children_info = st.text_area("Tell us about your children (ages, diagnoses, interests)", 
                value=st.session_state.user_profile.get("children_info", ""),
                placeholder="e.g., Sarah (8) - Autism, loves art and music; Michael (5) - ADHD, enjoys sports")
            
            if st.form_submit_button("💾 Save Profile"):
                st.session_state.user_profile.update({
                    "parent_name": parent_name,
                    "family_size": family_size,
                    "location": location,
                    "primary_language": primary_language,
                    "support_network": support_network,
                    "children_info": children_info,
                    "last_updated": date.today()
                })
                st.success("✅ Profile saved successfully!")
                st.rerun()
    
    with tab2:
        st.markdown("### ⚙️ App Preferences")
        
        with st.form("preferences"):
            col1, col2 = st.columns(2)
            
            with col1:
                notifications = st.checkbox("Enable notifications", 
                    value=st.session_state.user_profile.get("notifications", True))
                public_milestones = st.checkbox("Share milestones publicly by default", 
                    value=st.session_state.user_profile.get("public_milestones", True))
                crisis_alerts = st.checkbox("Enable crisis support alerts", 
                    value=st.session_state.user_profile.get("crisis_alerts", True))
            
            with col2:
                theme = st.selectbox("App Theme", ["Light", "Dark", "Auto"],
                    index=0 if not st.session_state.user_profile.get("theme") else 
                    ["Light", "Dark", "Auto"].index(st.session_state.user_profile.get("theme", "Light")))
                timezone = st.selectbox("Timezone", 
                    ["Eastern", "Central", "Mountain", "Pacific", "Alaska", "Hawaii"],
                    index=0 if not st.session_state.user_profile.get("timezone") else 
                    ["Eastern", "Central", "Mountain", "Pacific", "Alaska", "Hawaii"].index(st.session_state.user_profile.get("timezone", "Eastern")))
            
            if st.form_submit_button("💾 Save Preferences"):
                st.session_state.user_profile.update({
                    "notifications": notifications,
                    "public_milestones": public_milestones,
                    "crisis_alerts": crisis_alerts,
                    "theme": theme,
                    "timezone": timezone
                })
                st.success("✅ Preferences saved!")
                st.rerun()
    
    with tab3:
        st.markdown("### 📊 Account Statistics")
        
        if st.session_state.user_profile:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("📅 Member Since", 
                    st.session_state.user_profile.get("last_updated", "Today"))
                st.metric("🎉 Milestones Shared", len(st.session_state.milestone_shares))
                st.metric("📞 Emergency Contacts", len(st.session_state.emergency_contacts))
            
            with col2:
                st.metric("📋 Crisis Plans", len(st.session_state.crisis_plans))
                st.metric("📚 Saved Resources", len(st.session_state.saved_resources))
                
                # Calculate engagement score
                engagement_score = (
                    len(st.session_state.milestone_shares) * 10 +
                    len(st.session_state.emergency_contacts) * 5 +
                    len(st.session_state.crisis_plans) * 15 +
                    len(st.session_state.saved_resources) * 2
                )
                st.metric("🌟 Engagement Score", engagement_score)
        else:
            st.info("Complete your profile to see statistics!")

# --- Milestone Tracking Page ---
elif selected_page == "🎉 Milestone Tracking":
    st.markdown('<h2 class="section-header">🎉 Milestone Tracking & Community</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🎯 Track Milestones", "🌟 Community Celebrations"])
    
    with tab1:
        st.markdown("### 🎯 Share a New Milestone")
        
        with st.form("milestone_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                milestone_text = st.text_area("Describe the milestone", 
                    placeholder="e.g., 'My daughter said her first full sentence today!'")
                milestone_type = st.selectbox("Milestone Type", 
                    ["Communication", "Educational", "Social", "Medical", "Behavioral", "Daily Living"])
            
            with col2:
                child_age_milestone = st.text_input("Child's age (optional)")
                share_publicly = st.checkbox("Share with community", value=True)
            
            if st.form_submit_button("🎉 Share Milestone"):
                if milestone_text:
                    new_milestone_share = {
                        "text": milestone_text,
                        "type": milestone_type,
                        "child_age": child_age_milestone,
                        "shared_by": st.session_state.user_profile.get("parent_name", "Anonymous"),
                        "date": date.today(),
                        "public": share_publicly,
                        "celebrations": 0
                    }
                    
                    st.session_state.milestone_shares.append(new_milestone_share)
                    
                    st.success("🎉 Milestone shared! The community celebrates with you!")
                    st.balloons()
                    st.rerun()
    
    with tab2:
        # Display shared milestones
        if st.session_state.milestone_shares:
            st.markdown("### 🎊 Recent Community Celebrations")
            
            for i, milestone in enumerate(sorted(st.session_state.milestone_shares, key=lambda x: x["date"], reverse=True)):
                if milestone.get("public", True):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            milestone_icon = {"Communication": "🗣️", "Educational": "📚", "Social": "👫", 
                                            "Medical": "🏥", "Behavioral": "🎯", "Daily Living": "🏠"}.get(milestone["type"], "🎉")
                            
                            st.write(f"{milestone_icon} **{milestone['text']}**")
                            
                            details = []
                            if milestone.get("child_age"):
                                details.append(f"Age: {milestone['child_age']}")
                            details.append(f"Type: {milestone['type']}")
                            details.append(f"Shared by {milestone['shared_by']}")
                            details.append(f"{milestone['date']}")
                            
                            st.caption(" • ".join(details))
                        
                        with col2:
                            if st.button("🎉 Celebrate!", key=f"celebrate_{i}"):
                                st.session_state.milestone_shares[i]["celebrations"] += 1
                                st.success("🎉")
                                st.rerun()
                            
                            celebrations = milestone.get("celebrations", 0)
                            if celebrations > 0:
                                st.write(f"🎉 {celebrations} celebration{'s' if celebrations > 1 else ''}")
                        
                        st.markdown("---")
        
        else:
            st.info("🎉 No milestones shared yet. Be the first to share a celebration!")

# --- Crisis Support Page ---
elif selected_page == "📱 Crisis Support":
    st.markdown('<h2 class="section-header">📱 Crisis Support & Emergency Resources</h2>', unsafe_allow_html=True)
    
    # Emergency header
    st.markdown("""
    <div class="emergency-card">
        <h3>🚨 In Case of Emergency</h3>
        <p><strong>If this is a life-threatening emergency, call 911 immediately.</strong></p>
        <p>For mental health crises: National Suicide Prevention Lifeline: <strong>988</strong></p>
        <p>Crisis Text Line: Text <strong>HOME</strong> to <strong>741741</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🆘 Immediate Help", "📞 Crisis Contacts", "🧠 Mental Health", "📋 Crisis Plans"])
    
    with tab1:
        st.markdown("### 🆘 Immediate Support Resources")
        
        # Quick access buttons
        st.markdown("#### 🔥 Quick Access")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🚨 Call 911", use_container_width=True, type="primary"):
                st.error("☎️ Calling 911 for emergency services...")
        
        with col2:
            if st.button("💭 Crisis Text", use_container_width=True):
                st.info("📱 Text HOME to 741741")
        
        with col3:
            if st.button("🧠 Mental Health Crisis", use_container_width=True):
                st.info("☎️ Call 988 - Suicide & Crisis Lifeline")
        
        with col4:
            if st.button("👮 Non-Emergency Police", use_container_width=True):
                st.info("Contact your local non-emergency line")
        
        # Situation-specific help
        st.markdown("### 🎯 Situation-Specific Resources")
        
        crisis_situations = {
            "Behavioral Crisis/Meltdown": {
                "icon": "🌪️",
                "immediate_steps": [
                    "Ensure safety for everyone present",
                    "Remove triggers if possible", 
                    "Use calm, reassuring voice",
                    "Try preferred calming strategies",
                    "Give space and time to de-escalate"
                ],
                "when_to_call": "Call 911 if there's risk of serious injury to self or others",
                "resources": [
                    "Autism Crisis Support: 1-800-4AUTISM",
                    "Local Crisis Mobile Response Team",
                    "Your child's behavioral therapist"
                ]
            },
            "Medical Emergency": {
                "icon": "🏥",
                "immediate_steps": [
                    "Call 911 immediately",
                    "Have medical information ready",
                    "Know current medications",
                    "Contact emergency contact person",
                    "Bring medical summary to hospital"
                ],
                "when_to_call": "For seizures, breathing problems, loss of consciousness, severe injury",
                "resources": [
                    "Poison Control: 1-800-222-1222",
                    "Your child's primary doctor",
                    "Nearest children's hospital emergency department"
                ]
            },
            "School Crisis": {
                "icon": "🏫",
                "immediate_steps": [
                    "Contact school administration immediately",
                    "Document the incident",
                    "Request immediate IEP/504 meeting",
                    "Know your rights",
                    "Consider temporary alternative placement"
                ],
                "when_to_call": "For suspension threats, safety concerns, or discrimination",
                "resources": [
                    "Special Education Attorney",
                    "State Department of Education Complaint Line",
                    "Disability Rights Organizations"
                ]
            },
            "Mental Health Crisis": {
                "icon": "🧠",
                "immediate_steps": [
                    "Stay with the person",
                    "Listen without judgment",
                    "Remove means of self-harm",
                    "Call crisis line for guidance",
                    "Seek immediate professional help"
                ],
                "when_to_call": "For suicidal thoughts, self-harm, or severe depression/anxiety",
                "resources": [
                    "988 Suicide & Crisis Lifeline",
                    "Crisis Text Line: 741741",
                    "Local emergency mental health services"
                ]
            }
        }
        
        for situation, info in crisis_situations.items():
            with st.expander(f"{info['icon']} {situation}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Immediate Steps:**")
                    for step in info["immediate_steps"]:
                        st.write(f"• {step}")
                    
                    st.markdown(f"**When to Call 911:** {info['when_to_call']}")
                
                with col2:
                    st.markdown("**Key Resources:**")
                    for resource in info["resources"]:
                        st.write(f"• {resource}")
                
                # Quick action button
                if st.button(f"📞 Get Help for {situation}", key=f"help_{situation}"):
                    st.info(f"Connecting you with {situation.lower()} resources...")
    
    with tab2:
        st.markdown("### 📞 Emergency Contact Directory")
        
        # Personal emergency contacts
        st.markdown("#### 👨‍👩‍👧‍👦 Your Personal Emergency Contacts")
        
        with st.expander("➕ Add Emergency Contact"):
            with st.form("emergency_contact"):
                col1, col2 = st.columns(2)
                
                with col1:
                    contact_name = st.text_input("Name*")
                    contact_phone = st.text_input("Phone Number*")
                    contact_relationship = st.selectbox("Relationship", 
                        ["Spouse/Partner", "Parent/Guardian", "Sibling", "Extended Family", 
                         "Doctor", "Therapist", "Teacher", "Neighbor", "Friend", "Other"])
                
                with col2:
                    contact_email = st.text_input("Email (optional)")
                    contact_address = st.text_area("Address (optional)")
                    contact_notes = st.text_area("Special Notes", 
                        placeholder="e.g., 'Has key to house', 'Knows child's routine', 'Available 24/7'")
                
                primary_contact = st.checkbox("Primary emergency contact")
                
                if st.form_submit_button("Add Contact"):
                    if contact_name and contact_phone:
                        new_emergency_contact = {
                            "name": contact_name,
                            "phone": contact_phone,
                            "email": contact_email,
                            "relationship": contact_relationship,
                            "address": contact_address,
                            "notes": contact_notes,
                            "primary": primary_contact,
                            "added_date": date.today()
                        }
                        st.session_state.emergency_contacts.append(new_emergency_contact)
                        st.success(f"✅ Emergency contact {contact_name} added!")
                        st.rerun()
        
        # Display emergency contacts
        if st.session_state.emergency_contacts:
            primary_contacts = [c for c in st.session_state.emergency_contacts if c.get("primary", False)]
            other_contacts = [c for c in st.session_state.emergency_contacts if not c.get("primary", False)]
            
            if primary_contacts:
                st.markdown("**🔴 Primary Emergency Contacts:**")
                for i, contact in enumerate(primary_contacts):
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**{contact['name']}** - {contact['relationship']}")
                            if contact.get('notes'):
                                st.write(f"*{contact['notes']}*")
                        
                        with col2:
                            st.write(f"📞 {contact['phone']}")
                            if contact.get('email'):
                                st.write(f"📧 {contact['email']}")
                        
                        with col3:
                            if st.button("📞 Call", key=f"call_primary_{i}"):
                                st.info(f"Calling {contact['name']}...")
                            if st.button("🗑️", key=f"delete_primary_{i}", help="Delete"):
                                st.session_state.emergency_contacts.remove(contact)
                                st.rerun()
            
            if other_contacts:
                st.markdown("**📞 Other Emergency Contacts:**")
                for i, contact in enumerate(other_contacts):
                    with st.expander(f"📞 {contact['name']} - {contact['relationship']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Phone:** {contact['phone']}")
                            if contact.get('email'):
                                st.write(f"**Email:** {contact['email']}")
                        with col2:
                            if contact.get('address'):
                                st.write(f"**Address:** {contact['address']}")
                            if contact.get('notes'):
                                st.write(f"**Notes:** {contact['notes']}")
        
        else:
            st.warning("⚠️ No emergency contacts added yet. Add at least one primary emergency contact.")
        
        # National crisis resources
        st.markdown("### 🇺🇸 National Crisis Resources")
        
        national_resources = [
            {"name": "911", "description": "Emergency services", "phone": "911", "type": "Emergency"},
            {"name": "988 Suicide & Crisis Lifeline", "description": "24/7 mental health crisis support", "phone": "988", "type": "Mental Health"},
            {"name": "Crisis Text Line", "description": "24/7 crisis support via text", "phone": "Text HOME to 741741", "type": "Mental Health"},
            {"name": "National Child Abuse Hotline", "description": "Report child abuse", "phone": "1-800-4-A-CHILD (1-800-422-4453)", "type": "Safety"},
            {"name": "Poison Control", "description": "24/7 poison emergency help", "phone": "1-800-222-1222", "type": "Medical"},
            {"name": "Autism Crisis & Safety Resources", "description": "Autism-specific crisis support", "phone": "1-800-4-AUTISM", "type": "Disability-Specific"},
            {"name": "NAMI Helpline", "description": "Mental health information and support", "phone": "1-800-950-NAMI (6264)", "type": "Mental Health"},
        ]
        
        for resource in national_resources:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{resource['name']}**")
                    st.write(resource['description'])
                
                with col2:
                    st.write(f"📞 **{resource['phone']}**")
                    st.write(f"Type: {resource['type']}")
                
                with col3:
                    if st.button("📞 Call", key=f"call_{resource['name']}"):
                        st.info(f"Calling {resource['name']}...")
                    if st.button("💾 Save", key=f"save_{resource['name']}"):
                        st.success("Saved to contacts!")
    
    with tab3:
        st.markdown("### 🧠 Mental Health Support")
        
        # Mental health assessment
        st.markdown("#### 📊 Quick Mental Health Check")
        
        with st.form("mental_health_check"):
            st.write("How are you feeling right now? (This information is private and not shared)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                stress_level = st.select_slider("Stress Level", 
                    options=["Very Low", "Low", "Moderate", "High", "Very High"])
                energy_level = st.select_slider("Energy Level",
                    options=["Very Low", "Low", "Moderate", "High", "Very High"])
                mood = st.selectbox("Overall Mood", 
                    ["Very Good", "Good", "Neutral", "Low", "Very Low"])
            
            with col2:
                sleep_quality = st.selectbox("Sleep Quality", 
                    ["Excellent", "Good", "Fair", "Poor", "Very Poor"])
                support_feeling = st.selectbox("Feeling Supported", 
                    ["Very Supported", "Supported", "Neutral", "Unsupported", "Very Unsupported"])
                coping_ability = st.selectbox("Ability to Cope", 
                    ["Very Well", "Well", "Okay", "Struggling", "Very Struggling"])
            
            additional_concerns = st.text_area("Any additional concerns or thoughts?")
            
            if st.form_submit_button("Submit Check-in"):
                # Store the mental health check
                mental_health_entry = {
                    "date": date.today(),
                    "stress_level": stress_level,
                    "energy_level": energy_level,
                    "mood": mood,
                    "sleep_quality": sleep_quality,
                    "support_feeling": support_feeling,
                    "coping_ability": coping_ability,
                    "additional_concerns": additional_concerns
                }
                
                if "mental_health_checks" not in st.session_state:
                    st.session_state.mental_health_checks = []
                st.session_state.mental_health_checks.append(mental_health_entry)
                
                st.success("✅ Mental health check-in recorded. Thank you for taking care of yourself!")
                
                # Provide recommendations based on responses
                if stress_level in ["High", "Very High"] or mood in ["Low", "Very Low"]:
                    st.warning("⚠️ It looks like you might be experiencing some challenges. Consider reaching out for support.")
                    st.info("💡 Immediate self-care suggestions: Take deep breaths, call a friend, go for a walk, or practice mindfulness.")
    
    with tab4:
        st.markdown("### 📋 Crisis Response Plans")
        
        # Create new crisis plan
        with st.expander("➕ Create New Crisis Plan"):
            with st.form("crisis_plan"):
                plan_name = st.text_input("Plan Name", placeholder="e.g., 'Behavioral Meltdown Plan'")
                crisis_type = st.selectbox("Crisis Type", 
                    ["Behavioral", "Medical", "Mental Health", "School", "Safety", "Other"])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    warning_signs = st.text_area("Warning Signs", 
                        placeholder="List early warning signs that indicate this crisis may be developing...")
                    immediate_steps = st.text_area("Immediate Response Steps", 
                        placeholder="Step-by-step actions to take when crisis occurs...")
                
                with col2:
                    contacts_to_call = st.text_area("Who to Contact", 
                        placeholder="List people/services to contact in order of priority...")
                    resources_needed = st.text_area("Resources/Items Needed", 
                        placeholder="List any specific items, medications, or resources needed...")
                
                notes = st.text_area("Additional Notes", 
                    placeholder="Any other important information...")
                
                if st.form_submit_button("💾 Save Crisis Plan"):
                    if plan_name and immediate_steps:
                        new_crisis_plan = {
                            "name": plan_name,
                            "type": crisis_type,
                            "warning_signs": warning_signs,
                            "immediate_steps": immediate_steps,
                            "contacts_to_call": contacts_to_call,
                            "resources_needed": resources_needed,
                            "notes": notes,
                            "created_date": date.today(),
                            "last_used": None
                        }
                        st.session_state.crisis_plans.append(new_crisis_plan)
                        st.success(f"✅ Crisis plan '{plan_name}' saved!")
                        st.rerun()
        
        # Display existing crisis plans
        if st.session_state.crisis_plans:
            st.markdown("### 📋 Your Crisis Plans")
            
            for i, plan in enumerate(st.session_state.crisis_plans):
                with st.expander(f"📋 {plan['name']} ({plan['type']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**⚠️ Warning Signs:**")
                        st.write(plan['warning_signs'])
                        
                        st.markdown("**🚨 Immediate Steps:**")
                        st.write(plan['immediate_steps'])
                    
                    with col2:
                        st.markdown("**📞 Contacts to Call:**")
                        st.write(plan['contacts_to_call'])
                        
                        st.markdown("**🎒 Resources Needed:**")
                        st.write(plan['resources_needed'])
                    
                    if plan['notes']:
                        st.markdown("**📝 Additional Notes:**")
                        st.write(plan['notes'])
                    
                    # Action buttons
                    button_col1, button_col2, button_col3 = st.columns(3)
                    
                    with button_col1:
                        if st.button("🚨 Activate Plan", key=f"activate_{i}"):
                            st.session_state.crisis_plans[i]["last_used"] = date.today()
                            st.success(f"✅ Crisis plan '{plan['name']}' activated!")
                            st.info("📞 Remember to follow the contact list and immediate steps outlined in your plan.")
                    
                    with button_col2:
                        if st.button("✏️ Edit", key=f"edit_{i}"):
                            st.info("Edit functionality would open the plan for editing...")
                    
                    with button_col3:
                        if st.button("🗑️ Delete", key=f"delete_plan_{i}"):
                            st.session_state.crisis_plans.pop(i)
                            st.success("Crisis plan deleted!")
                            st.rerun()
        
        else:
            st.info("📋 No crisis plans created yet. Create your first plan to be prepared for emergencies.")

# --- Resources & Forms Page ---
elif selected_page == "📚 Resources & Forms":
    st.markdown('<h2 class="section-header">📚 Resources & Forms</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Educational Resources", "📋 Forms & Templates", "🔗 External Links"])
    
    with tab1:
        st.markdown("### 📖 Educational Resources")
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Search resources", placeholder="Enter keywords...")
        
        with col2:
            resource_category = st.selectbox("Category", 
                ["All", "Autism", "ADHD", "Learning Disabilities", "Behavioral", "Medical", "Legal", "Educational"])
        
        with col3:
            resource_type = st.selectbox("Type", 
                ["All", "Article", "Video", "Webinar", "Podcast", "Book", "Guide", "Checklist"])
        
        # Sample resources
        sample_resources = [
            {
                "title": "Understanding IEP vs 504 Plans",
                "description": "Comprehensive guide to special education services and accommodations",
                "type": "Guide",
                "category": "Educational",
                "topics": ["IEP", "504 Plan", "Special Education", "Accommodations"],
                "length": "15 min read",
                "rating": 4.8,
                "url": "#"
            },
            {
                "title": "Autism Sensory Strategies",
                "description": "Practical strategies for managing sensory challenges in daily life",
                "type": "Article",
                "category": "Autism",
                "topics": ["Sensory Processing", "Autism", "Daily Living", "Strategies"],
                "length": "10 min read",
                "rating": 4.9,
                "url": "#"
            },
            {
                "title": "ADHD Medication Guide",
                "description": "Understanding medication options and side effects for ADHD",
                "type": "Guide",
                "category": "ADHD",
                "topics": ["ADHD", "Medication", "Treatment", "Side Effects"],
                "length": "20 min read",
                "rating": 4.7,
                "url": "#"
            },
            {
                "title": "Behavioral Intervention Strategies",
                "description": "Evidence-based approaches to managing challenging behaviors",
                "type": "Video",
                "category": "Behavioral",
                "topics": ["Behavior", "Intervention", "ABA", "Strategies"],
                "length": "45 min watch",
                "rating": 4.6,
                "url": "#"
            }
        ]
        
        # Filter resources based on search and category
        filtered_resources = sample_resources
        
        if search_term:
            filtered_resources = [r for r in filtered_resources 
                                if search_term.lower() in r['title'].lower() or 
                                   search_term.lower() in r['description'].lower() or
                                   any(search_term.lower() in topic.lower() for topic in r['topics'])]
        
        if resource_category != "All":
            filtered_resources = [r for r in filtered_resources if r['category'] == resource_category]
        
        if resource_type != "All":
            filtered_resources = [r for r in filtered_resources if r['type'] == resource_type]
        
        # Display resources
        if filtered_resources:
            for resource in filtered_resources:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**📄 {resource['title']}**")
                        st.write(resource['description'])
                        topics_text = " • ".join(resource['topics'])
                        st.write(f"**Topics:** {topics_text}")
                        
                    with col2:
                        st.write(f"**Type:** {resource['type']}")
                        st.write(f"**Length:** {resource['length']}")
                        rating_stars = "⭐" * int(resource['rating'])
                        st.write(f"**Rating:** {rating_stars} {resource['rating']}")
                    
                    with col3:
                        if st.button("📖 Read Now", key=f"read_{resource['title']}"):
                            st.info("Opening resource viewer...")
                        if st.button("💾 Save", key=f"save_{resource['title']}"):
                            if resource not in st.session_state.saved_resources:
                                st.session_state.saved_resources.append(resource)
                                st.success("Saved to your library!")
                            else:
                                st.info("Already in your library!")
                    
                    st.markdown("---")
        else:
            st.info("No resources found matching your criteria. Try adjusting your search or filters.")
    
    with tab2:
        st.markdown("### 📋 Forms & Templates")
        
        # Template categories
        template_categories = {
            "IEP & 504 Planning": [
                "IEP Meeting Preparation Checklist",
                "IEP Goal Tracking Sheet", 
                "504 Plan Request Template",
                "Parent Input Form for IEP",
                "Transition Assessment Form"
            ],
            "Medical & Therapy": [
                "Medical History Summary",
                "Therapy Progress Tracker", 
                "Medication Log Template",
                "Doctor Visit Preparation Form",
                "Insurance Appeal Letter Template"
            ],
            "Daily Living": [
                "Behavior Support Plan Template",
                "Daily Schedule Visual",
                "Chore Chart Template",
                "Social Stories Template",
                "Communication Board Template"
            ],
            "Legal & Advocacy": [
                "Special Education Complaint Form",
                "Due Process Request Template",
                "Accommodation Request Letter",
                "Meeting Documentation Form",
                "Rights Violation Report"
            ]
        }
        
        for category, templates in template_categories.items():
            with st.expander(f"📁 {category}"):
                col1, col2 = st.columns(2)
                
                for i, template in enumerate(templates):
                    with col1 if i % 2 == 0 else col2:
                        st.write(f"📄 **{template}**")
                        
                        template_col1, template_col2 = st.columns(2)
                        with template_col1:
                            if st.button("📥 Download", key=f"download_{template}"):
                                st.success(f"Downloaded {template}!")
                        with template_col2:
                            if st.button("👁️ Preview", key=f"preview_{template}"):
                                st.info(f"Previewing {template}...")
    
    with tab3:
        st.markdown("### 🔗 Helpful External Links")
        
        external_links = {
            "Government Resources": [
                {"name": "IDEA - Individuals with Disabilities Education Act", "url": "https://sites.ed.gov/idea/"},
                {"name": "Office for Civil Rights", "url": "https://www2.ed.gov/about/offices/list/ocr/"},
                {"name": "Social Security Disability Benefits", "url": "https://www.ssa.gov/disability/"},
                {"name": "Centers for Disease Control - Developmental Disabilities", "url": "https://www.cdc.gov/ncbddd/developmentaldisabilities/"}
            ],
            "National Organizations": [
                {"name": "Autism Society", "url": "https://autismsociety.org/"},
                {"name": "National Down Syndrome Society", "url": "https://www.ndss.org/"},
                {"name": "CHADD - ADHD Support", "url": "https://chadd.org/"},
                {"name": "National Association for Mental Illness (NAMI)", "url": "https://nami.org/"}
            ],
            "Educational Support": [
                {"name": "Understood.org", "url": "https://www.understood.org/"},
                {"name": "Wrightslaw - Special Education Law", "url": "https://www.wrightslaw.com/"},
                {"name": "Council of Parent Attorneys and Advocates", "url": "https://www.copaa.org/"},
                {"name": "National Center for Learning Disabilities", "url": "https://www.ncld.org/"}
            ]
        }
        
        for category, links in external_links.items():
            with st.expander(f"🔗 {category}"):
                for link in links:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{link['name']}**")
                    with col2:
                        if st.button("🔗 Visit", key=f"visit_{link['name']}"):
                            st.info(f"Opening {link['name']}...")

# --- Progress Analytics Page ---
elif selected_page == "📊 Progress Analytics":
    st.markdown('<h2 class="section-header">📊 Progress Analytics</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Milestone Trends", "🧠 Mental Health Tracking", "📋 Activity Summary"])
    
    with tab1:
        st.markdown("### 📈 Milestone Progress Over Time")
        
        if st.session_state.milestone_shares:
            # Create milestone data for visualization
            milestone_data = []
            for milestone in st.session_state.milestone_shares:
                milestone_data.append({
                    "Date": milestone["date"],
                    "Type": milestone["type"],
                    "Celebrations": milestone.get("celebrations", 0)
                })
            
            df = pd.DataFrame(milestone_data)
            
            # Milestone count by type
            st.markdown("#### 🎯 Milestones by Type")
            milestone_counts = df['Type'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                for milestone_type, count in milestone_counts.items():
                    st.metric(milestone_type, count)
            
            with col2:
                # Simple bar chart representation
                st.write("**Distribution:**")
                for milestone_type, count in milestone_counts.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"{milestone_type}: {count} ({percentage:.1f}%)")
            
            # Recent milestone activity
            st.markdown("#### 📅 Recent Activity")
            recent_milestones = sorted(st.session_state.milestone_shares, key=lambda x: x["date"], reverse=True)[:5]
            
            for milestone in recent_milestones:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{milestone['text'][:50]}...**" if len(milestone['text']) > 50 else f"**{milestone['text']}**")
                with col2:
                    st.write(f"{milestone['type']}")
                with col3:
                    st.write(f"{milestone['date']}")
        
        else:
            st.info("📊 No milestone data available yet. Start sharing milestones to see your progress!")
    
    with tab2:
        st.markdown("### 🧠 Mental Health Trends")
        
        if "mental_health_checks" in st.session_state and st.session_state.mental_health_checks:
            # Display recent mental health trends
            recent_checks = sorted(st.session_state.mental_health_checks, key=lambda x: x["date"], reverse=True)[:5]
            
            st.markdown("#### 📊 Recent Check-ins")
            
            for check in recent_checks:
                with st.expander(f"Check-in from {check['date']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Stress Level:** {check['stress_level']}")
                        st.write(f"**Energy Level:** {check['energy_level']}")
                        st.write(f"**Mood:** {check['mood']}")
                    
                    with col2:
                        st.write(f"**Sleep Quality:** {check['sleep_quality']}")
                        st.write(f"**Feeling Supported:** {check['support_feeling']}")
                        st.write(f"**Coping Ability:** {check['coping_ability']}")
                    
                    if check.get('additional_concerns'):
                        st.write(f"**Additional Concerns:** {check['additional_concerns']}")
            
            # Simple trend indicators
            if len(recent_checks) >= 2:
                st.markdown("#### 📈 Trend Indicators")
                
                latest = recent_checks[0]
                previous = recent_checks[1]
                
                stress_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
                mood_levels = ["Very Good", "Good", "Neutral", "Low", "Very Low"]
                
                latest_stress_idx = stress_levels.index(latest['stress_level'])
                previous_stress_idx = stress_levels.index(previous['stress_level'])
                
                latest_mood_idx = mood_levels.index(latest['mood'])
                previous_mood_idx = mood_levels.index(previous['mood'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if latest_stress_idx < previous_stress_idx:
                        st.success("📉 Stress levels are improving!")
                    elif latest_stress_idx > previous_stress_idx:
                        st.warning("📈 Stress levels have increased")
                    else:
                        st.info("➡️ Stress levels are stable")
                
                with col2:
                    if latest_mood_idx < previous_mood_idx:
                        st.success("😊 Mood is improving!")
                    elif latest_mood_idx > previous_mood_idx:
                        st.warning("😔 Mood has declined")
                    else:
                        st.info("➡️ Mood is stable")
        
        else:
            st.info("🧠 No mental health check-ins recorded yet. Complete a check-in in the Crisis Support section to track your wellbeing.")
    
    with tab3:
        st.markdown("### 📋 Activity Summary")
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎉 Total Milestones", len(st.session_state.milestone_shares))
        
        with col2:
            st.metric("📞 Emergency Contacts", len(st.session_state.emergency_contacts))
        
        with col3:
            st.metric("📋 Crisis Plans", len(st.session_state.crisis_plans))
        
        with col4:
            mental_health_checks = len(st.session_state.get("mental_health_checks", []))
            st.metric("🧠 Mental Health Check-ins", mental_health_checks)
        
        # Activity breakdown
        st.markdown("#### 📊 Activity Breakdown")
        
        if st.session_state.milestone_shares:
            # Milestone celebrations received
            total_celebrations = sum(milestone.get("celebrations", 0) for milestone in st.session_state.milestone_shares)
            st.write(f"🎉 **Total Celebrations Received:** {total_celebrations}")
            
            # Most celebrated milestone
            if total_celebrations > 0:
                most_celebrated = max(st.session_state.milestone_shares, key=lambda x: x.get("celebrations", 0))
                st.write(f"🏆 **Most Celebrated Milestone:** {most_celebrated['text'][:50]}... ({most_celebrated.get('celebrations', 0)} celebrations)")
        
        # Profile completion
        st.markdown("#### ✅ Profile Completion")
        
        profile_items = [
            ("Parent Name", bool(st.session_state.user_profile.get("parent_name"))),
            ("Family Information", bool(st.session_state.user_profile.get("children_info"))),
            ("Emergency Contacts", len(st.session_state.emergency_contacts) > 0),
            ("Crisis Plans", len(st.session_state.crisis_plans) > 0),
            ("Milestones Shared", len(st.session_state.milestone_shares) > 0)
        ]
        
        completed_items = sum(1 for _, completed in profile_items if completed)
        completion_percentage = (completed_items / len(profile_items)) * 100
        
        st.progress(completion_percentage / 100)
        st.write(f"**Profile Completion: {completion_percentage:.0f}%**")
        
        for item_name, completed in profile_items:
            status = "✅" if completed else "❌"
            st.write(f"{status} {item_name}")
        
        # Recommendations
        st.markdown("#### 💡 Recommendations")
        
        recommendations = []
        
        if len(st.session_state.emergency_contacts) == 0:
            recommendations.append("Add at least one emergency contact for safety")
        
        if len(st.session_state.crisis_plans) == 0:
            recommendations.append("Create a crisis response plan to be prepared")
        
        if not st.session_state.user_profile.get("parent_name"):
            recommendations.append("Complete your profile information")
        
        if len(st.session_state.milestone_shares) == 0:
            recommendations.append("Share your first milestone with the community")
        
        mental_health_checks = st.session_state.get("mental_health_checks", [])
        if len(mental_health_checks) == 0:
            recommendations.append("Complete a mental health check-in to track your wellbeing")
        
        if recommendations:
            for rec in recommendations:
                st.write(f"💡 {rec}")
        else:
            st.success("🎉 Great job! You're making full use of the support hub!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🌟 <strong>Special Needs Parenting Support Hub</strong> 🌟</p>
    <p>You're not alone in this journey. We're here to support you every step of the way.</p>
    <p><em>Remember: You are your child's best advocate, and you're doing an amazing job!</em></p>
</div>
""", unsafe_allow_html=True)

