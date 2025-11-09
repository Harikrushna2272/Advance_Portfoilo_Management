# decision_engine.py
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime

from src.agents.fundamentals_agent import analyze_fundamentals
from src.agents.technicals_agent import analyze_technicals
from src.agents.valuation_agent import analyze_valuation
from src.agents.sentiment_agent import analyze_sentiment
from src.agents.risk_manager import analyze_risk
from src.agents.portfolio_manager import analyze_portfolio
from src.models.ensemble_model import EnsembleRLModel
from src.utils.data_preprocessor import get_processed_features_for_rl
from src.utils.config import ENSEMBLE_MODEL_PATHS


class DecisionEngine:
    """
    Advanced decision engine that combines 6 analytical agents with 5-model ensemble RL
    for final buy/sell/hold decisions.
    """
    
    def __init__(self):
        self.ensemble_model = None
        self.decision_history = []
        self.performance_metrics = {
            "total_decisions": 0,
            "correct_predictions": 0,
            "accuracy": 0.0
        }
        
    def load_ensemble_model(self):
        """Load the 5-model ensemble RL system."""
        try:
            self.ensemble_model = EnsembleRLModel(ENSEMBLE_MODEL_PATHS)
            print("✅ 5-Model Ensemble RL loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error loading ensemble model: {e}")
            return False
    
    def run_comprehensive_analysis(self, stock: str, stock_data: pd.DataFrame, 
                                 start_date: str, end_date: str, 
                                 portfolio: Dict) -> Dict:
        """
        Run all 6 agents + 5-model ensemble RL analysis.
        
        Returns:
            Dict with all analysis results and final decision
        """
        print(f"\n🔍 Running comprehensive analysis for {stock}...")
        
        # Initialize results structure
        analysis_results = {
            "stock": stock,
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "ensemble_rl": {},
            "final_decision": {},
            "confidence_scores": {},
            "risk_assessment": {}
        }
        
        try:
            # 1. Run all 6 analytical agents
            print("📊 Running 6 analytical agents...")
            
            # Fundamentals Agent
            fundamentals = analyze_fundamentals(stock, end_date)
            analysis_results["agents"]["fundamentals"] = fundamentals
            
            # Technicals Agent  
            technicals = analyze_technicals(stock, start_date, end_date)
            analysis_results["agents"]["technicals"] = technicals
            
            # Valuation Agent
            valuation = analyze_valuation(stock, end_date)
            analysis_results["agents"]["valuation"] = valuation
            
            # Sentiment Agent
            sentiment = analyze_sentiment(stock, end_date)
            analysis_results["agents"]["sentiment"] = sentiment
            
            # Risk Manager
            risk = analyze_risk(stock, start_date, end_date, portfolio)
            analysis_results["agents"]["risk"] = risk
            
            # Portfolio Manager
            portfolio_decision = analyze_portfolio(
                {
                    "fundamentals_agent": {stock: fundamentals},
                    "technicals_agent": {stock: technicals},
                    "valuation_agent": {stock: valuation},
                    "sentiment_agent": {stock: sentiment},
                    "risk_manager": {stock: risk}
                },
                portfolio,
                [stock]
            )
            analysis_results["agents"]["portfolio"] = portfolio_decision.get(stock, {})
            
            # 2. Run 5-model ensemble RL
            print("🤖 Running 5-model ensemble RL...")
            
            if self.ensemble_model is None:
                if not self.load_ensemble_model():
                    analysis_results["ensemble_rl"] = {"error": "Failed to load ensemble model"}
                    return analysis_results
            
            # Get preprocessed features for RL
            rl_features = get_processed_features_for_rl(stock_data)
            
            if rl_features is not None:
                # Get ensemble prediction with details
                rl_details = self.ensemble_model.predict_with_details(rl_features)
                
                analysis_results["ensemble_rl"] = {
                    "prediction": rl_details["ensemble_prediction"],
                    "signal": rl_details["ensemble_signal"],
                    "model_votes": rl_details["model_votes"],
                    "vote_counts": rl_details["vote_counts"],
                    "features_used": len(rl_features),
                    "model_count": len(self.ensemble_model.models)
                }
            else:
                analysis_results["ensemble_rl"] = {"error": "Failed to preprocess features"}
            
            # 3. Generate final decision
            print("🎯 Generating final decision...")
            final_decision = self._generate_final_decision(analysis_results)
            analysis_results["final_decision"] = final_decision
            
            # 4. Calculate confidence scores
            confidence_scores = self._calculate_confidence_scores(analysis_results)
            analysis_results["confidence_scores"] = confidence_scores
            
            # 5. Risk assessment
            risk_assessment = self._assess_risk(analysis_results, portfolio)
            analysis_results["risk_assessment"] = risk_assessment
            
            # 6. Update performance metrics
            self._update_performance_metrics(analysis_results)
            
            print(f"✅ Analysis complete for {stock}")
            return analysis_results
            
        except Exception as e:
            print(f"❌ Error in comprehensive analysis: {e}")
            analysis_results["error"] = str(e)
            return analysis_results
    
    def _generate_final_decision(self, analysis_results: Dict) -> Dict:
        """
        Generate final buy/sell/hold decision using new flow:
        4 Agents → 5 RL Models (20% each) → Portfolio Manager
        
        Flow:
        1. 4 Agents provide signals (no weights)
        2. 5 RL Models get equal 20% weight each
        3. Portfolio Manager decides final quantity
        """
        try:
            print("🎯 Generating final decision using new flow...")
            
            # Step 1: Collect 4 Agent signals (no weights)
            agent_signals = {}
            agent_confidences = {}
            
            # Get signals from 4 core agents
            core_agents = ["fundamentals", "technicals", "valuation", "sentiment", "risk"]
            
            for agent_name in core_agents:
                if agent_name in analysis_results["agents"]:
                    result = analysis_results["agents"][agent_name]
                    if isinstance(result, dict) and "signal" in result:
                        agent_signals[agent_name] = result["signal"]
                        agent_confidences[agent_name] = result.get("confidence", 50)
                        print(f"📊 {agent_name.title()}: {result['signal']} ({result.get('confidence', 50)}%)")
            
            # Step 2: Get 5 RL Models ensemble decision (20% each)
            rl_decision = self._get_rl_ensemble_decision(analysis_results)
            
            # Step 3: Combine 4 Agents + 5 RL Models for Portfolio Manager input
            combined_signals = {
                "agent_signals": agent_signals,
                "agent_confidences": agent_confidences,
                "rl_decision": rl_decision
            }
            
            # Step 4: Portfolio Manager makes final decision
            final_decision = self._portfolio_manager_decision(combined_signals, analysis_results)
            
            return final_decision
            
        except Exception as e:
            print(f"❌ Error generating final decision: {e}")
            return {
                "signal": "HOLD",
                "confidence": 0,
                "quantity": 0,
                "error": str(e)
            }
    
    def _get_rl_ensemble_decision(self, analysis_results: Dict) -> Dict:
        """
        Get decision from 5 RL Models with equal 20% weight each.
        """
        try:
            print("🤖 Getting 5 RL Models ensemble decision...")
            
            if "ensemble_rl" not in analysis_results or "error" in analysis_results["ensemble_rl"]:
                print("❌ No RL ensemble data available")
                return {"signal": "HOLD", "confidence": 0, "model_votes": {}}
            
            # Get individual model predictions from ensemble_rl results
            ensemble_signal = analysis_results["ensemble_rl"]["signal"]
            ensemble_prediction = analysis_results["ensemble_rl"]["prediction"]
            model_votes = analysis_results["ensemble_rl"]["model_votes"]
            vote_counts = analysis_results["ensemble_rl"]["vote_counts"]
            
            # Calculate weighted score (20% each = 0.2 each)
            rl_weights = {"SAC": 0.2, "PPO": 0.2, "A2C": 0.2, "DQN": 0.2, "TD3": 0.2}
            
            weighted_score = 0
            for model, vote in model_votes.items():
                weighted_score += vote * rl_weights[model]
            
            # Determine RL ensemble signal
            if weighted_score > 0.1:
                rl_signal = "BUY"
                rl_confidence = min(95, abs(weighted_score) * 100)
            elif weighted_score < -0.1:
                rl_signal = "SELL"
                rl_confidence = min(95, abs(weighted_score) * 100)
            else:
                rl_signal = "HOLD"
                rl_confidence = 50
            
            print(f"🎯 RL Ensemble: {rl_signal} (confidence: {rl_confidence}%, score: {weighted_score:.3f})")
            print(f"📊 Model Votes: {model_votes}")
            
            return {
                "signal": rl_signal,
                "confidence": rl_confidence,
                "weighted_score": weighted_score,
                "model_votes": model_votes
            }
            
        except Exception as e:
            print(f"❌ Error in RL ensemble decision: {e}")
            return {"signal": "HOLD", "confidence": 0, "model_votes": {}}
    
    def _portfolio_manager_decision(self, combined_signals: Dict, analysis_results: Dict) -> Dict:
        """
        Portfolio Manager makes final decision based on 4 Agents + 5 RL Models.
        Decides signal and quantity.
        """
        try:
            print("🎯 Portfolio Manager making final decision...")
            
            agent_signals = combined_signals["agent_signals"]
            agent_confidences = combined_signals["agent_confidences"]
            rl_decision = combined_signals["rl_decision"]
            
            # Count signals from 4 agents
            signal_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
            total_confidence = 0
            
            for agent, signal in agent_signals.items():
                if signal in ["bullish", "BUY", "buy"]:
                    signal_counts["bullish"] += 1
                elif signal in ["bearish", "SELL", "sell"]:
                    signal_counts["bearish"] += 1
                else:
                    signal_counts["neutral"] += 1
                
                total_confidence += agent_confidences.get(agent, 50)
            
            # Calculate average agent confidence
            avg_agent_confidence = total_confidence / len(agent_signals) if agent_signals else 50
            
            # Determine agent consensus
            if signal_counts["bullish"] > signal_counts["bearish"] and signal_counts["bullish"] > signal_counts["neutral"]:
                agent_consensus = "bullish"
            elif signal_counts["bearish"] > signal_counts["bullish"] and signal_counts["bearish"] > signal_counts["neutral"]:
                agent_consensus = "bearish"
            else:
                agent_consensus = "neutral"
            
            # Combine agent consensus with RL decision
            rl_signal = rl_decision["signal"]
            rl_confidence = rl_decision["confidence"]
            
            # Final decision logic
            if agent_consensus == "bullish" and rl_signal == "BUY":
                final_signal = "BUY"
                final_confidence = min(95, (avg_agent_confidence + rl_confidence) / 2)
                quantity_multiplier = 1.0
            elif agent_consensus == "bearish" and rl_signal == "SELL":
                final_signal = "SELL"
                final_confidence = min(95, (avg_agent_confidence + rl_confidence) / 2)
                quantity_multiplier = 1.0
            elif agent_consensus == "bullish" or rl_signal == "BUY":
                final_signal = "BUY"
                final_confidence = min(90, (avg_agent_confidence + rl_confidence) / 2 * 0.8)
                quantity_multiplier = 0.7
            elif agent_consensus == "bearish" or rl_signal == "SELL":
                final_signal = "SELL"
                final_confidence = min(90, (avg_agent_confidence + rl_confidence) / 2 * 0.8)
                quantity_multiplier = 0.7
            else:
                final_signal = "HOLD"
                final_confidence = 50
                quantity_multiplier = 0
            
            # Calculate quantity based on confidence and risk
            base_quantity = 100  # Base quantity
            quantity = int(base_quantity * (final_confidence / 100) * quantity_multiplier)
            
            # Risk adjustment
            risk_signal = agent_signals.get("risk", "neutral")
            if risk_signal == "bearish":
                quantity = int(quantity * 0.5)  # Reduce quantity for high risk
            elif risk_signal == "bullish":
                quantity = int(quantity * 1.2)  # Increase quantity for low risk
            
            # Cap quantity
            quantity = max(0, min(quantity, 500))  # Cap between 0 and 500
            
            print(f"🎯 Final Decision: {final_signal}")
            print(f"📊 Confidence: {final_confidence:.1f}%")
            print(f"📦 Quantity: {quantity}")
            print(f"📈 Agent Consensus: {agent_consensus} ({signal_counts})")
            print(f"🤖 RL Decision: {rl_signal} ({rl_confidence}%)")
            
            return {
                "signal": final_signal,
                "confidence": round(final_confidence, 2),
                "quantity": quantity,
                "agent_consensus": agent_consensus,
                "agent_signal_counts": signal_counts,
                "rl_decision": rl_decision,
                "quantity_multiplier": quantity_multiplier,
                "reasoning": self._generate_portfolio_reasoning(agent_consensus, rl_signal, signal_counts, final_confidence)
            }
            
        except Exception as e:
            print(f"❌ Error in portfolio manager decision: {e}")
            return {
                "signal": "HOLD",
                "confidence": 0,
                "quantity": 0,
                "error": str(e)
            }
    
    def _generate_portfolio_reasoning(self, agent_consensus: str, rl_signal: str, signal_counts: Dict, confidence: float) -> str:
        """Generate reasoning for portfolio manager decision."""
        try:
            reasoning_parts = []
            
            # Agent consensus reasoning
            if agent_consensus == "bullish":
                reasoning_parts.append(f"Strong bullish consensus from agents ({signal_counts['bullish']} bullish signals)")
            elif agent_consensus == "bearish":
                reasoning_parts.append(f"Strong bearish consensus from agents ({signal_counts['bearish']} bearish signals)")
            else:
                reasoning_parts.append(f"Mixed signals from agents (bullish: {signal_counts['bullish']}, bearish: {signal_counts['bearish']}, neutral: {signal_counts['neutral']})")
            
            # RL decision reasoning
            reasoning_parts.append(f"RL ensemble suggests {rl_signal}")
            
            # Final decision reasoning
            if agent_consensus == "bullish" and rl_signal == "BUY":
                reasoning_parts.append("Strong alignment between agents and RL - high confidence trade")
            elif agent_consensus == "bearish" and rl_signal == "SELL":
                reasoning_parts.append("Strong alignment between agents and RL - high confidence trade")
            elif agent_consensus in ["bullish", "bearish"] or rl_signal in ["BUY", "SELL"]:
                reasoning_parts.append("Partial alignment - moderate confidence trade")
            else:
                reasoning_parts.append("No clear directional signal - holding position")
            
            return " | ".join(reasoning_parts)
            
        except Exception as e:
            return f"Reasoning unavailable: {e}"
    
    def _calculate_position_size(self, confidence: float, analysis_results: Dict) -> float:
        """Calculate position size based on confidence and risk assessment."""
        try:
            # Base position size (percentage of portfolio)
            base_size = 0.05  # 5% base position
            
            # Adjust based on confidence
            confidence_multiplier = confidence / 100
            
            # Adjust based on risk assessment
            risk_signal = analysis_results["agents"].get("risk", {}).get("signal", "neutral")
            if risk_signal == "bearish":
                risk_multiplier = 0.5  # Reduce position for high risk
            elif risk_signal == "bullish":
                risk_multiplier = 1.2  # Increase position for low risk
            else:
                risk_multiplier = 1.0
            
            # Calculate final position size
            position_size = base_size * confidence_multiplier * risk_multiplier
            
            # Cap at maximum 10% of portfolio
            return min(0.10, max(0.01, position_size))
            
        except Exception as e:
            print(f"❌ Error calculating position size: {e}")
            return 0.05  # Default 5%
    
    def _generate_reasoning(self, analysis_results: Dict, final_signal: str) -> str:
        """Generate human-readable reasoning for the decision."""
        try:
            reasoning_parts = []
            
            # Add agent insights
            for agent_name, result in analysis_results["agents"].items():
                if isinstance(result, dict) and "signal" in result:
                    signal = result["signal"]
                    confidence = result.get("confidence", 50)
                    reasoning_parts.append(f"{agent_name.title()}: {signal} ({confidence}%)")
            
            # Add ensemble RL insight
            if "ensemble_rl" in analysis_results and "signal" in analysis_results["ensemble_rl"]:
                rl_signal = analysis_results["ensemble_rl"]["signal"]
                reasoning_parts.append(f"Ensemble RL: {rl_signal}")
            
            # Add final decision reasoning
            if final_signal == "BUY":
                reasoning_parts.append("Strong bullish consensus across multiple agents")
            elif final_signal == "SELL":
                reasoning_parts.append("Strong bearish consensus across multiple agents")
            else:
                reasoning_parts.append("Mixed signals or insufficient confidence for directional trade")
            
            return " | ".join(reasoning_parts)
            
        except Exception as e:
            return f"Decision reasoning unavailable: {e}"
    
    def _assess_risk_level(self, score: float, confidence: float) -> str:
        """Assess risk level of the decision."""
        if confidence < 60:
            return "HIGH"
        elif confidence < 80:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_confidence_scores(self, analysis_results: Dict) -> Dict:
        """Calculate various confidence metrics."""
        try:
            confidences = []
            
            # Collect agent confidences
            for agent_name, result in analysis_results["agents"].items():
                if isinstance(result, dict) and "confidence" in result:
                    confidences.append(result["confidence"])
            
            # Calculate statistics
            if confidences:
                avg_confidence = np.mean(confidences)
                max_confidence = np.max(confidences)
                min_confidence = np.min(confidences)
                std_confidence = np.std(confidences)
            else:
                avg_confidence = max_confidence = min_confidence = std_confidence = 0
            
            return {
                "average": round(avg_confidence, 2),
                "maximum": round(max_confidence, 2),
                "minimum": round(min_confidence, 2),
                "standard_deviation": round(std_confidence, 2),
                "agent_count": len(confidences)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _assess_risk(self, analysis_results: Dict, portfolio: Dict) -> Dict:
        """Assess overall risk of the decision."""
        try:
            risk_factors = []
            
            # Portfolio concentration risk
            total_positions = len(portfolio.get("positions", {}))
            if total_positions > 10:
                risk_factors.append("High portfolio concentration")
            
            # Cash availability
            cash = portfolio.get("cash", 0)
            if cash < 10000:  # Less than $10k cash
                risk_factors.append("Low cash reserves")
            
            # Signal divergence
            signals = []
            for agent_name, result in analysis_results["agents"].items():
                if isinstance(result, dict) and "signal" in result:
                    signals.append(result["signal"])
            
            if len(set(signals)) > 2:  # More than 2 different signals
                risk_factors.append("High signal divergence")
            
            # Confidence dispersion
            confidences = []
            for agent_name, result in analysis_results["agents"].items():
                if isinstance(result, dict) and "confidence" in result:
                    confidences.append(result["confidence"])
            
            if confidences and np.std(confidences) > 20:
                risk_factors.append("High confidence dispersion")
            
            return {
                "risk_factors": risk_factors,
                "risk_level": "HIGH" if len(risk_factors) > 2 else "MEDIUM" if len(risk_factors) > 0 else "LOW",
                "recommendation": "Proceed with caution" if risk_factors else "Proceed normally"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _update_performance_metrics(self, analysis_results: Dict):
        """Update performance tracking metrics."""
        try:
            self.decision_history.append(analysis_results)
            self.performance_metrics["total_decisions"] += 1
            
            # Keep only last 100 decisions for performance tracking
            if len(self.decision_history) > 100:
                self.decision_history = self.decision_history[-100:]
            
        except Exception as e:
            print(f"❌ Error updating performance metrics: {e}")
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary of the decision engine."""
        try:
            if not self.decision_history:
                return {"message": "No decisions made yet"}
            
            # Calculate accuracy (simplified - would need actual market data for real accuracy)
            recent_decisions = self.decision_history[-10:]  # Last 10 decisions
            
            return {
                "total_decisions": self.performance_metrics["total_decisions"],
                "recent_decisions": len(recent_decisions),
                "average_confidence": np.mean([d["final_decision"].get("confidence", 0) for d in recent_decisions]),
                "signal_distribution": {
                    "BUY": sum(1 for d in recent_decisions if d["final_decision"].get("signal") == "BUY"),
                    "SELL": sum(1 for d in recent_decisions if d["final_decision"].get("signal") == "SELL"),
                    "HOLD": sum(1 for d in recent_decisions if d["final_decision"].get("signal") == "HOLD")
                }
            }
            
        except Exception as e:
            return {"error": str(e)}


def create_decision_engine() -> DecisionEngine:
    """Factory function to create and initialize decision engine."""
    engine = DecisionEngine()
    engine.load_ensemble_model()
    return engine
