import streamlit as st
import requests

# Your FastAPI URL (replace with your actual ngrok URL)
FASTAPI_URL = "https://7d00-116-110-42-45.ngrok-free.app"

st.title("Car Search App")

# Input for the user to enter the search query
query = st.text_input("Enter your car search query:")

if st.button("Search"):
    if query:
        # Send a POST request with the query in the body
        response = requests.post(
            f"{FASTAPI_URL}/search",
            json={"query": query}  # Sending the query in JSON format
        )

        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                st.write("### Search Results:")

                # Display the search criteria used
                st.write("### Search Criteria:")
                search_criteria = data.get("search_criteria", {})
                if search_criteria:
                    if "make" in search_criteria:
                        st.write(f"**Make**: {search_criteria['make']}")
                    if "country" in search_criteria:
                        st.write(f"**Country**: {', '.join(search_criteria['country'])}")
                    if "date_filter" in search_criteria:
                        date_filter = search_criteria["date_filter"]
                        if "gte" in date_filter:
                            st.write(f"**Year After**: {date_filter['gte'] - 1}")
                        elif "lte" in date_filter:
                            st.write(f"**Year Before**: {date_filter['lte']}")

                # Display the car search results
                st.write("### Cars Found:")
                for car_data in data["results"]:
                    car = car_data["_source"]  # Access the '_source' field containing car details
                    st.write(f"**Make**: {car['make']}")
                    st.write(f"**Model**: {car['model']}")
                    st.write(f"**Year**: {car['year']}")
                    st.write(f"**Price**: ${car['price']}")
                    st.write(f"**Country**: {car['country']}")
                    st.write(f"**Description**: {car['description']}")
                    st.write("---")
            else:
                st.write("No results found.")
        else:
            st.write(f"Error: {response.status_code} - {response.text}")
    else:
        st.write("Please enter a query.")
