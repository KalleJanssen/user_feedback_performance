echo "Creating classification data"
python3 create_classification_data.py

echo "Creating topic modeling data"
python3 create_topic_modeling_data.py

echo "Creating sentiment data"
python3 create_sentiment_data.py

echo "Creating similarity data"
python3 create_similarity_data.py