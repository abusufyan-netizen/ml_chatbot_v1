import streamlit as st
from PIL import Image, ImageOps
import numpy as np, os, time, json
import tensorflow as tf
from streamlit_drawable_canvas import st_canvas
from utils.drive_auth import DriveAuth
from utils.data_manager import save_feedback_image, preprocess_pil, load_model_safe
from utils.backup_utils import backup_all_to_drive
import pandas as pd

st.set_page_config(page_title='Digit Recognition AI', layout='wide')
st.markdown('<style>body{background:#0e1117;color:#fafafa}</style>', unsafe_allow_html=True)

BASE = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, 'model', 'digit_model.h5')
HISTORY_FILE = os.path.join(BASE, 'logs', 'history.json')
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

# Load model
model = load_model_safe(MODEL_PATH)

# Drive auth instance
drive = DriveAuth(credentials_path=os.path.join(BASE, 'credentials', 'credentials.json'))

# Sidebar - navigation
page = st.sidebar.selectbox('Pages', ['Dashboard','Dataset Manager','History','Accuracy Monitor','Drive Settings','Admin'])

# Dashboard
if page == 'Dashboard':
    st.header('🤖 Digit Recognition AI - Dashboard')
    col1, col2 = st.columns([1,1])
    with col1:
        uploaded = st.file_uploader('Upload image', type=['png','jpg','jpeg'])
        st.markdown('**Or draw below**')
        canvas = st_canvas(fill_color='rgba(255,255,255,1)', stroke_width=12, stroke_color='#ffffff', background_color='#000000', height=260, width=260, drawing_mode='freedraw', key='canvas1')
        if st.button('Recognize'):
            pil = None
            if uploaded:
                pil = Image.open(uploaded).convert('L')
            else:
                if canvas and canvas.image_data is not None:
                    pil = Image.fromarray(canvas.image_data.astype('uint8'), 'RGBA').convert('L')
            if pil is None:
                st.warning('Provide an image or drawing.')
            else:
                arr, proc = preprocess_pil(pil)
                if model is None:
                    st.error('Model not loaded. Place digit_model.h5 in model/')
                else:
                    preds = model.predict(arr)
                    pred = int(np.argmax(preds[0])); conf = float(np.max(preds[0]))*100.0
                    st.image(proc.resize((140,140)), caption='Processed (28x28)')
                    st.success(f'Predicted: {pred} (Confidence: {conf:.2f}%)')
                    # feedback
                    if st.button('✅ Correct'):
                        # log as correct
                        rec = {'ts': time.time(), 'predicted': pred, 'correct': pred, 'status':'correct'}
                        history = []
                        if os.path.exists(HISTORY_FILE):
                            history = json.load(open(HISTORY_FILE))
                        history.append(rec); json.dump(history, open(HISTORY_FILE,'w'), indent=2)
                        st.success('Saved as correct.')
                    if st.button('❌ Incorrect'):
                        label = st.number_input('Enter correct label', min_value=0, max_value=9, step=1)
                        if st.button('Submit label'):
                            # save feedback image and log
                            path = save_feedback_image(proc, int(label))
                            rec = {'ts': time.time(), 'predicted': pred, 'correct': int(label), 'status':'incorrect', 'path': path}
                            history = []
                            if os.path.exists(HISTORY_FILE):
                                history = json.load(open(HISTORY_FILE))
                            history.append(rec); json.dump(history, open(HISTORY_FILE,'w'), indent=2)
                            st.success('Feedback saved.')
    with col2:
        st.info('Model status and quick actions')
        st.write('Model path:', MODEL_PATH)
        st.write('Drive connected:', drive.is_authenticated())
        if st.button('Backup now (manual)'):
            ok, msg = backup_all_to_drive(local_dir=os.path.dirname(BASE), drive_auth=drive)
            if ok:
                st.success('Backup complete')
            else:
                st.error('Backup failed: '+msg)

# Simple other pages
if page == 'Dataset Manager':
    st.header('Dataset Manager')
    up = st.file_uploader('Upload dataset image', type=['png','jpg','jpeg'])
    label = st.number_input('Label (0-9)', min_value=0, max_value=9, step=1)
    if st.button('Add to dataset'):
        if up:
            img = Image.open(up).convert('L').resize((28,28))
            p = os.path.join(BASE,'dataset', f'manual_{int(time.time())}.png')
            img.save(p)
            st.success('Saved to dataset: '+p)
        else:
            st.warning('Upload an image first.')

if page == 'History':
    st.header('Prediction History')
    if os.path.exists(HISTORY_FILE):
        history = json.load(open(HISTORY_FILE))
        df = pd.DataFrame(history)
        st.dataframe(df)
    else:
        st.info('No history yet.')

if page == 'Accuracy Monitor':
    st.header('Accuracy Monitor')
    st.write('This page will show training history and metrics (placeholder).')
    if os.path.exists(os.path.join(BASE,'logs','training_history.json')):
        th = json.load(open(os.path.join(BASE,'logs','training_history.json')))
        st.write(th)
    else:
        st.info('No training history found.')

if page == 'Drive Settings':
    st.header('Drive Settings')
    st.write('Authenticated:', drive.is_authenticated())
    if not drive.is_authenticated():
        st.write('Upload credentials.json to enable Drive integration.')
        cred = st.file_uploader('Upload credentials.json', type=['json'])
        if cred is not None:
            data = cred.read()
            with open(os.path.join(BASE,'credentials','credentials.json'), 'wb') as f:
                f.write(data)
            st.success('Saved credentials. Reload app to authenticate.')
    else:
        st.success('Drive is available. Backup folder: Digit_Recognition_AI_Backup')

if page == 'Admin':
    st.header('Admin')
    if st.button('Show model summary'):
        if model is not None:
            st.text(str(model.summary()))
        else:
            st.warning('Model not loaded.')
