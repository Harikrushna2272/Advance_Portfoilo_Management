"""Knowledge graph utilities for enhanced sentiment analysis."""
import networkx as nx
from typing import Dict, List, Tuple
import pandas as pd
from datetime import datetime
import spacy
import numpy as np

class CompanyKnowledgeGraph:
    def __init__(self):
        """Initialize the knowledge graph."""
        self.graph = nx.DiGraph()
        self.nlp = spacy.load("en_core_web_sm")
        
    def build_graph(self, company_data: Dict, news_data: List[Dict], relationships: List[Dict]):
        """Build knowledge graph from company data, news, and relationships."""
        # Add company node
        self.graph.add_node(company_data["symbol"], 
                           type="company",
                           sector=company_data.get("sector"),
                           industry=company_data.get("industry"))
        
        # Add news nodes and relationships
        for idx, news in enumerate(news_data):
            news_id = f"news_{idx}"
            sentiment_score = self._analyze_news_sentiment(news["text"])
            self.graph.add_node(news_id, 
                              type="news",
                              date=news["date"],
                              sentiment=sentiment_score)
            self.graph.add_edge(company_data["symbol"], news_id, type="has_news")
        
        # Add relationship nodes
        for rel in relationships:
            self.graph.add_node(rel["company"],
                              type="company")
            self.graph.add_edge(company_data["symbol"],
                              rel["company"],
                              type=rel["relationship_type"],
                              strength=rel["strength"])
    
    def _analyze_news_sentiment(self, text: str) -> float:
        """Analyze sentiment of news text using spaCy."""
        doc = self.nlp(text)
        # Simple sentiment scoring based on positive/negative words
        sentiment_score = 0
        for token in doc:
            if token.pos_ in ["ADJ", "VERB"]:
                # Add more sophisticated sentiment scoring here
                pass
        return sentiment_score
    
    def get_sentiment_score(self) -> Tuple[str, float]:
        """Calculate overall sentiment score from the knowledge graph."""
        sentiment_scores = []
        
        # Get direct news sentiment
        news_nodes = [n for n in self.graph.nodes if self.graph.nodes[n]["type"] == "news"]
        if news_nodes:
            news_sentiments = [self.graph.nodes[n]["sentiment"] for n in news_nodes]
            sentiment_scores.append(np.mean(news_sentiments))
        
        # Consider relationship impacts
        company_nodes = [n for n in self.graph.nodes if self.graph.nodes[n]["type"] == "company"]
        for node in company_nodes:
            if node == list(self.graph.nodes)[0]:  # Skip the main company
                continue
            edge_data = self.graph.get_edge_data(list(self.graph.nodes)[0], node)
            if edge_data:
                relationship_impact = edge_data["strength"]
                sentiment_scores.append(relationship_impact)
        
        # Calculate final sentiment
        if not sentiment_scores:
            return "neutral", 50.0
            
        avg_sentiment = np.mean(sentiment_scores)
        confidence = min(abs(avg_sentiment) * 100, 100)
        
        if avg_sentiment > 0.2:
            return "bullish", confidence
        elif avg_sentiment < -0.2:
            return "bearish", confidence
        else:
            return "neutral", confidence
