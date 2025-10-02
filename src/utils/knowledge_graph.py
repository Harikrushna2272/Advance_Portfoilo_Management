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
        """Analyze sentiment of news text using spaCy.
        
        Uses NLP features including:
        - Named Entity Recognition (NER)
        - Part-of-speech tagging
        - Dependency parsing
        - Word vectors for semantic analysis
        """
        doc = self.nlp(text)
        sentiment_score = 0.0
        
        # Initialize sentiment dictionaries
        financial_pos_words = {
            "surge", "gain", "rise", "improve", "profit", "growth", "exceed",
            "outperform", "breakthrough", "innovative", "successful", "positive"
        }
        financial_neg_words = {
            "decline", "drop", "fall", "loss", "debt", "risk", "downgrade",
            "underperform", "recession", "negative", "bankruptcy", "litigation"
        }
        
        # Weight multipliers for different aspects
        ENTITY_WEIGHT = 1.5      # Weight for named entities
        NEGATION_WEIGHT = -1.0   # Weight for negation
        INTENSITY_WEIGHT = 1.2    # Weight for intensity modifiers
        
        # Analyze each sentence
        for sent in doc.sents:
            sent_score = 0.0
            negation = False
            intensity = 1.0
            
            # Check for named entities (companies, organizations)
            entities = [ent for ent in sent.ents if ent.label_ in ["ORG", "PERSON", "GPE"]]
            entity_multiplier = ENTITY_WEIGHT if entities else 1.0
            
            # Analyze tokens in sentence
            for token in sent:
                # Check for negation
                if token.dep_ == "neg":
                    negation = True
                    continue
                
                # Check for intensity modifiers
                if token.pos_ == "ADV" and token.head.pos_ in ["ADJ", "VERB"]:
                    if token.text.lower() in ["very", "highly", "extremely", "significantly"]:
                        intensity = INTENSITY_WEIGHT
                
                # Get base word sentiment
                word_score = 0.0
                if token.text.lower() in financial_pos_words:
                    word_score = 1.0
                elif token.text.lower() in financial_neg_words:
                    word_score = -1.0
                
                # Apply dependency-based analysis
                if token.pos_ in ["ADJ", "VERB"]:
                    # Check for subject-verb or verb-object relationships
                    if token.dep_ in ["ROOT", "acomp", "xcomp"]:
                        word_score *= 1.2  # Boost score for main predicates
                
                # Consider word vectors for unknown words
                if word_score == 0 and token.has_vector:
                    # Compare with known positive/negative words using vector similarity
                    pos_sim = max([token.similarity(self.nlp(pos_word)) 
                                 for pos_word in list(financial_pos_words)[:5]])
                    neg_sim = max([token.similarity(self.nlp(neg_word)) 
                                 for neg_word in list(financial_neg_words)[:5]])
                    if pos_sim > 0.6:  # Threshold for similarity
                        word_score = pos_sim
                    elif neg_sim > 0.6:
                        word_score = -neg_sim
                
                # Apply modifiers
                word_score *= intensity
                if negation:
                    word_score *= NEGATION_WEIGHT
                
                sent_score += word_score
            
            # Apply entity multiplier to sentence score
            sent_score *= entity_multiplier
            sentiment_score += sent_score
        
        # Normalize score to range [-1, 1]
        num_sents = len(list(doc.sents))
        if num_sents > 0:
            sentiment_score = max(min(sentiment_score / num_sents, 1.0), -1.0)
            
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
