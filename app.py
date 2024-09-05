#import streamlit as st

#st.header('Tossing a Coin')

#st.write('It is not a functional application yet. Under construction.')

#number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
#start_button = st.button('Run')

#if start_button:
#    st.write(f'Running the experiment of {number_of_trials} trials.')

#st.write('It is not a functional application yet. Under construction.')
import pandas as pd #I just added this pandas and line 19 to 25 at step 4 (after creating the True buttom)
import scipy.stats
import streamlit as st
import time

# these are stateful variables which are preserved as Streamlin reruns this script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

#The title
st.header('Tossing Coins')
#The canvas chart
chart = st.line_chart([0.5])

def toss_coin(n):

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no +=1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean
#The number of trials buttom
number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experient of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1 #FinalStep5 and line 56 to the end.
    mean = toss_coin(number_of_trials) #This line code is to get the True value when clicking the bottom.tosscoinasstartbuttom.txt
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iterations', 'mean'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = \
        st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
