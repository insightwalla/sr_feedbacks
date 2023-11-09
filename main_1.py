import streamlit as st
import pandas as pd
from google_big_query  import GoogleBigQuery


def adding_data():
    # create a list of week years from jan 2023
    dates = pd.date_range(start='2022-12-01', end=pd.to_datetime('today').date(), freq='D')
    dates = pd.DataFrame(dates, columns=['date'])
    dates['week_year'] = dates['date'].apply(lambda x: 'W' + str(x.week) + 'Y' + str(x.year))
    dates = dates.groupby('week_year').agg({'date': ['min', 'max']})
    # sort by ascending date
    dates = dates.sort_values(ascending=False, by=[('date', 'min')]) 
    # now create a dict with the week year as key and the min and max date as value
    week_year_dict = {}
    for index, row in dates.iterrows():
        week_year_dict[index] = {
            'start_date': row['date']['min'].date(),
            'end_date': row['date']['max'].date()
        }

    c1,c2 = st.columns(2)
    # use it for the selectbox
    week_years = list(week_year_dict.keys())
    week_year = c1.selectbox('Choose the week year', week_years, index=0)
    start_date = week_year_dict[week_year]['start_date']
    end_date = week_year_dict[week_year]['end_date']
    
    # create a st.date_input
    st.write(str(start_date),' / ', str(end_date))
    # as d/m/y
    start_date = start_date.strftime('%m/%d/%Y')
    end_date = end_date.strftime('%m/%d/%Y')
    # select the venues

    venues = {
        'Dishoom Covent Garden': '`jp-gs-379412.sevenrooms_covent_garden.reservation_feedback`' ,
        'Dishoom Shoreditch': '`jp-gs-379412.sevenrooms_shoreditch.reservation_feedback`',
        'Dishoom Kings Cross': '`jp-gs-379412.sevenrooms_kings_cross.reservation_feedback`',
        'Dishoom Carnaby': '`jp-gs-379412.sevenrooms_carnaby.reservation_feedback`',
        'Dishoom Edinburgh': '`jp-gs-379412.sevenrooms_edinburgh.reservation_feedback`',
        'Dishoom Kensington': '`jp-gs-379412.sevenrooms_kensington.reservation_feedback`',
        'Dishoom Manchester': '`jp-gs-379412.sevenrooms_manchester.reservation_feedback`',
        'Dishoom Birmingham': '`jp-gs-379412.sevenrooms_birmingham.reservation_feedback`',
        'Dishoom Canary Wharf': '`jp-gs-379412.sevenrooms_canary_wharf.reservation_feedback`',
        'Dishoom Permit Room Brighton': '`jp-gs-379412.sevenrooms_permit_room_brighton.reservation_feedback`'
        }
        # use it to query the data
        
    with st.form('query'):
        venues_list = list(venues.keys()) + ['All']
        venue = c2.selectbox('Choose the venue', venues_list, index=0)
        if venue != 'All':
            query = f'''
            select
                *
            from
                {venues[venue]}
            where
                reservation_date >= '{start_date}'
                and reservation_date <= '{end_date}'
            '''
        else:
            query = ''
            for i, v in enumerate(venues.values()):
                # add the union all
                if i != 0:
                    query += 'union all '
                query += f'''
                select  
                    *
                from
                    {v}
                where
                    reservation_date >= '{start_date}'
                    and reservation_date <= '{end_date}'
                '''

        submit = st.form_submit_button(f'Fetch **{venue}** (**{start_date}** - **{end_date}**)', use_container_width=True, type='primary')
        if submit:
            with st.spinner('Fetching data...'):
                data = GoogleBigQuery().query(query)
            
            if len(data) == 0:
                st.info('No data found for the selected dates')
                st.stop()

            st.toast('Data fetched successfully', icon='✅')
            # show the data
            st.write(f'**{venue}** (**{start_date}** - **{end_date}**)')
            st.write(f'Found **{len(data)}** reviews')
            st.dataframe(data)

            # get unique venues
            if venue == 'All':
                unique_venues = data['venue'].unique().tolist()
                tabs = st.tabs(unique_venues)
                for i, venue in enumerate(unique_venues):
                    with tabs[i]:
                        data_venue = data[data['venue'] == venue]
                        st.write(f'**{venue}** (**{start_date}** - **{end_date}**)')
                        st.write(f'Found **{len(data_venue)}** reviews')
                        st.dataframe(data_venue)

            st.stop()

if __name__ == '__main__':
    adding_data()