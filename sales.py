import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration for wide mode
st.set_page_config(
    page_title="Truherb Sales Performance", #Sets the app name to Truherb Sales Performance
    layout="wide",  # Enables wide mode
)

st.markdown(
    """
    <style>
    .css-18e3th9 { 
        padding-top: 1rem;  /* Removes padding for the main content */
        padding-bottom: 1rem;  /* Keeps some bottom padding */
    }
    .css-1d391kg {
        padding-top: 1.1rem;  /* Removes padding for the header section */
    }
    .css-1vq4p4l {
        padding-top: 1.1rem;  /* Removes top margin for main container */
    }
    .block-container {
        padding-top: 1.2rem; /* Ensures no padding in the container */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to fetch data from a public Google Sheet
def fetch_sales_data():
    try:
        # Correct URL for the CSV export of the sheet
        sheet_url = "https://docs.google.com/spreadsheets/d/13A0RVgb7uRW93RXEWN7RSH5i97jShgHnYB4zmvcThpk/gviz/tq?tqx=out:csv&gid=1502421750"
        
        # Read data into a DataFrame
        df = pd.read_csv(sheet_url)

        # Columns to clean (monetary values)
        monetary_cols = ['sept24_rev_gen', 'oct24_rev_gen', 'nov24_rev_gen', 
                         'sept24_target', 'oct24_target', 'nov24_target']
        
        # Clean monetary columns: remove $, replace empty with 0, and convert to float
        for col in monetary_cols:
            if col in df.columns:  # Ensure the column exists
                df[col] = (
                    df[col]
                    .fillna("0")  # Replace missing values with "0"
                    .replace('[\$,]', '', regex=True)  # Remove $ and commas
                    .replace('', '0')  # Handle remaining empty strings
                )
                try:
                    df[col] = df[col].astype(float)  # Convert to float
                except ValueError:
                    st.error(f"Unable to convert column {col} to float. Check for invalid data.")
            else:
                st.warning(f"Column '{col}' is missing in the dataset.")
        
        # Columns for inquiries (replace NaNs with 0)
        inquiry_cols = ['sept24_inq_no', 'oct24_inq_no', 'nov24_inq_no']
        for col in inquiry_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0).astype(int)
            else:
                st.warning(f"Column '{col}' is missing in the dataset.")

        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# User database with usernames and passwords
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "thomas": {"password": "thomas123", "role": "user"},
    "max": {"password": "max123", "role": "user"},
    "kelvin": {"password": "kelvin123", "role": "user"},
    "soumya": {"password": "soumya123", "role": "user"},
    "rishika": {"password": "rishika123", "role": "user"},
    "akon": {"password": "akon123", "role": "user"},
    "andrew": {"password": "andrew123", "role": "user"},
    "eddy": {"password": "eddy123", "role": "user"},
    "june": {"password": "june123", "role": "user"},
    "rony": {"password": "rony123", "role": "user"},
    "daisy": {"password": "daisy123", "role": "user"},
    "priyanka": {"password": "priyanka123", "role": "user"},
    "annie": {"password": "annie123", "role": "user"},
    "eric": {"password": "eric123", "role": "user"},
    "karisma": {"password": "karisma123", "role": "user"},
    "preetam": {"password": "preetam123", "role": "user"},
    "edward": {"password": "edward123", "role": "user"},
    "summit": {"password": "summit123", "role": "user"}
}

# Mapping usernames to corresponding agent names in the data
user_agent_mapping = {
    "thomas": "Thomas",
    "max": "Max",
    "kelvin": "Kelvin",
    "soumya": "Soumya",
    "rishika": "Rishika",
    "akon": "Akon",
    "andrew": "Andrew",
    "eddy": "Eddy",
    "june": "June",
    "rony": "Rony",
    "daisy": "Daisy",
    "priyanka": "Priyanka",
    "annie": "Annie",
    "eric": "Eric",
    "karisma": "Karisma",
    "preetam": "Preetam",
    "edward": "Edward",
    "summit": "Summit"
}

# Authentication function
def authenticate(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None

# Main app function
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.role == "admin":
            admin_page()
        else:
            user_page()

# Login page
def show_login_page():
    st.title("Login Page")
    st.subheader("Please log in to access your dashboard")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")

    if login_button:
        role = authenticate(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.username = username.capitalize()
            st.session_state.role = role
            st.rerun()  # Refresh the app to load the appropriate dashboard
        else:
            st.error("Invalid username or password.")

# Admin dashboard
def admin_page():
    st.header("Admin Dashboard")
    st.write(f"Welcome, {st.session_state.username}!. This is the admin panel where you can view all Users Performance.")
    # Fetch and display data
    df = fetch_sales_data()
    if not df.empty:
        # Prepare a summary for all users
        performance_data = []
        for _, row in df.iterrows():
            agent_name = row['agent_name']
            total_revenue = row[['sept24_rev_gen', 'oct24_rev_gen', 'nov24_rev_gen']].sum()
            total_target = row[['sept24_target', 'oct24_target', 'nov24_target']].sum()
            rating = calculate_rating(total_revenue, total_target)

            # Append to performance data
            performance_data.append({
                "Agent Name": agent_name,
                "September Revenue": f"${row['sept24_rev_gen']:,.2f}",
                "October Revenue": f"${row['oct24_rev_gen']:,.2f}",
                "November Revenue": f"${row['nov24_rev_gen']:,.2f}",
                "September Target": f"${row['sept24_target']:,.2f}",
                "October Target": f"${row['oct24_target']:,.2f}",
                "November Target": f"${row['nov24_target']:,.2f}",
                "Total Revenue": f"${total_revenue:,.2f}",
                "Total Target": f"${total_target:,.2f}",
                "Rating                                ": rating
            })

        # Convert performance data into a DataFrame for display
        summary_df = pd.DataFrame(performance_data)
        
        # Update the index to start from 1
        summary_df.index = range(1, len(summary_df) + 1)
        
        # Apply styling to increase the width of the "Rating" column
        styled_df = summary_df.style.set_table_styles(
            [
                {"selector": "thead th", "props": [("text-align", "center"), ("font-size", "14px")]},
                {"selector": "tbody td", "props": [("text-align", "center")]},
                {"selector": "tbody td:nth-child(10)", "props": [("min-width", "200px"), ("max-width", "300px"), ("text-align", "center")]}
            ]
        )

        # Display the table
        st.subheader("Users' Monthly Performance Summary")
        st.dataframe(summary_df, use_container_width=False)

        # Optionally, download the table as CSV
        csv = summary_df.to_csv(index=False)
        st.download_button(
            label="Download Performance Data as CSV",
            data=csv,
            file_name="performance_summary.csv",
            mime="text/csv"
        )
    else:
        st.error("No data available to display.")

    # Logout button
    if st.button("Logout"):
        logout()

def calculate_rating(total_revenue, total_target):
    """
    Calculate performance percentage and determine user rating.
    Updated to handle 0 revenue or target cases more effectively.
    """
    try:
        # Special cases
        if total_target == 0 and total_revenue == 0:
            return "No Target Set or Sales Data"
        elif total_target == 0:
            return "Target is zero; performance cannot be calculated."
        
        # Calculate performance percentage
        performance_percentage = (total_revenue / total_target) * 100

        # Determine underperformance or overperformance rating
        if performance_percentage < 0 or total_revenue == 0:
            # Underperformance ratings
            if performance_percentage <= -60 or total_revenue == 0:
                return "Critical"
            elif -60 < performance_percentage <= -40:
                return "Extremely Poor"
            elif -40 < performance_percentage <= -20:
                return "Poor"
            else:
                return "Deficient"
        else:
            # Overperformance ratings
            if 0 <= performance_percentage <= 25:
                return "High Roller"
            elif 25 < performance_percentage <= 75:
                return "Sales Hero"
            elif 75 < performance_percentage <= 150:
                return "Top Achievers"
            else:
                return "Star Performer"
    except Exception as e:
        return f"Error in calculation: {e}"

# User Dashboard
def user_page():
    st.header("User Dashboard")
    st.write(f"Welcome, {st.session_state.username}!")

    # Fetch and display data
    df = fetch_sales_data()
    if not df.empty:
        # Map logged-in user to agent name
        agent_name = user_agent_mapping.get(st.session_state.username.lower(), None)
        if agent_name:
            # Filter data for the specific agent
            user_data = df[df['agent_name'] == agent_name]
            if not user_data.empty:
                # Layout with 2 columns: left for chart, right for report
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Revenue vs. Target bar chart for the user
                    fig = go.Figure()

                    # Adding grouped bars for each month
                    months = ['September', 'October', 'November']
                    revenues = [
                        user_data['sept24_rev_gen'].values[0],
                        user_data['oct24_rev_gen'].values[0],
                        user_data['nov24_rev_gen'].values[0],
                    ]
                    targets = [
                        user_data['sept24_target'].values[0],
                        user_data['oct24_target'].values[0],
                        user_data['nov24_target'].values[0],
                    ]

                    # Add bars for Revenue
                    fig.add_trace(go.Bar(
                        name='Revenue',
                        x=months,
                        y=revenues,
                        text=[f"${val:,.0f}" for val in revenues],
                        textposition='outside',
                        marker_color='blue',
                        width=0.4
                    ))

                    # Add bars for Target
                    fig.add_trace(go.Bar(
                        name='Target',
                        x=months,
                        y=targets,
                        text=[f"${val:,.0f}" for val in targets],
                        textposition='outside',
                        marker_color='lightblue',
                        width=0.4
                    ))

                    # Update layout for improved visuals
                    fig.update_layout(
                        barmode='group',  # Grouped bar chart
                        title=dict(
                            text="Revenue vs. Target Comparison",
                            font=dict(size=20),
                        ),
                        xaxis=dict(
                            title="Month",
                            tickfont=dict(size=14),
                            title_font=dict(size=16),
                        ),
                        yaxis=dict(
                            title="Amount (USD)",
                            tickfont=dict(size=14),
                            title_font=dict(size=16),
                            gridcolor='lightgrey'  # Add subtle gridlines
                        ),
                        legend=dict(
                            x=0.5, y=-0.2,
                            orientation="h",
                            xanchor="center",
                            font=dict(size=12),
                        ),
                        bargap=0.2,  # Gap between bars
                        bargroupgap=0.3,  # Increase gap between groups
                        margin=dict(l=50, r=50, t=70, b=100),
                        height=500,
                    )

                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.subheader("User Report")
                    # Calculate total revenue and target
                    total_revenue = user_data[['sept24_rev_gen', 'oct24_rev_gen', 'nov24_rev_gen']].sum(axis=1).values[0]
                    total_target = user_data[['sept24_target', 'oct24_target', 'nov24_target']].sum(axis=1).values[0]

                    # Calculate performance and rating
                    rating = calculate_rating(total_revenue, total_target)

                    # Display the summary
                    st.write(f"**Total Revenue Generated:** ${total_revenue:,.2f}")
                    st.write(f"**Total Target Achieved:** ${total_target:,.2f}")
                    st.write(f"**Performance Rating:** {rating}")

            else:   
                st.error("No data found for your account.")
        else:
            st.error("Agent name not mapped to your username. Please contact admin.")

    if st.button("Logout"):
        logout()

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()  # Refresh the app to return to the login page

if __name__ == "__main__":
    main()
