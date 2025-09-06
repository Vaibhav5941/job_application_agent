# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# import streamlit as st
# from backend.database import fetch_applications


# st.title("📂 Past Applications")

# apps = fetch_applications()

# if apps:
#     for app in apps:
#         st.write(f"📌 Application ID: {app[0]}")
#         st.json(app[1])
#         st.write("📄 Cover Letter:")
#         st.write(app[2])
#         st.write(f"🕒 Date: {app[3]}")
#         st.divider()
        
# else:
#     st.info("No applications found in database.")
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
from backend.database import fetch_applications,delete_application


st.title("📂 Past Applications")

apps = fetch_applications()

if apps:
    for app in apps:
        app_id = app[0]
        st.write(f"📌 Application ID: {app_id}")
        st.json(app[1])
        st.write("📄 Cover Letter:")
        st.write(app[2])
        st.write(f"🕒 Date: {app[3]}")
        
        if st.button(f"🗑️ Delete Application {app_id}", key=f"delete_{app_id}"):
            delete_application(app_id)
            st.success(f"Application {app_id} deleted!")
            st.rerun()


        st.divider()
        
else:
    st.info("No applications found in database.")
