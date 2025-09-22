import joblib
import numpy as np
from typing import List, Dict, Any

class EnsembleRLModel:
    """
    5-Model Ensemble RL System for robust trading decisions.
    
    Models:
    - SAC (Soft Actor-Critic): Continuous action space, good for position sizing
    - PPO (Proximal Policy Optimization): Stable policy updates
    - A2C (Advantage Actor-Critic): Fast learning, good for real-time
    - DQN (Deep Q-Network): Discrete action space, good for buy/sell/hold
    - TD3 (Twin Delayed Deep Deterministic): Continuous control, robust
    """
    
    def __init__(self, model_paths: List[str]):
        self.models = []
        self.model_names = ["SAC", "PPO", "A2C", "DQN", "TD3"]
        self.loaded_models = {}
        
        print(f"🤖 Loading 5-Model Ensemble RL System...")
        
        for i, path in enumerate(model_paths):
            model_name = self.model_names[i] if i < len(self.model_names) else f"Model_{i+1}"
            try:
                model = joblib.load(path)
                self.models.append(model)
                self.loaded_models[model_name] = True
                print(f"✅ {model_name} loaded successfully from {path}")
            except Exception as e:
                print(f"❌ Error loading {model_name} from {path}: {e}")
                self.loaded_models[model_name] = False

        print(f"📊 Ensemble Status: {sum(self.loaded_models.values())}/{len(model_paths)} models loaded")
        
        if not self.models:
            print("⚠️  Warning: No models loaded successfully!")

    def predict(self, features: List[float]) -> int:
        """
        Make prediction using ensemble of 5 RL models.
        
        Args:
            features: List of 14 preprocessed features
            
        Returns:
            int: 1=BUY, -1=SELL, 0=HOLD
        """
        if not self.models:
            print("❌ No models available for prediction")
            return 0  # Default to HOLD
        
        # Collect predictions from all models
        predictions = []
        model_predictions = {}
        
        for i, model in enumerate(self.models):
            model_name = self.model_names[i] if i < len(self.model_names) else f"Model_{i+1}"
            try:
                pred = model.predict([features])[0]
                predictions.append(pred)
                model_predictions[model_name] = pred
                
                # Map prediction to signal for logging
                signal_map = {1: "BUY", -1: "SELL", 0: "HOLD"}
                signal = signal_map.get(pred, "UNKNOWN")
                print(f"🎯 {model_name}: {signal} (prediction: {pred})")
                
            except Exception as e:
                print(f"❌ Prediction error in {model_name}: {e}")
                model_predictions[model_name] = 0  # Default to HOLD
        
        if not predictions:
            print("❌ No valid predictions from any model")
            return 0  # Default to HOLD
        
        # Majority voting: 1=BUY, -1=SELL, 0=HOLD
        ensemble_prediction = int(np.sign(np.sum(predictions)))
        
        # Log ensemble decision
        signal_map = {1: "BUY", -1: "SELL", 0: "HOLD"}
        ensemble_signal = signal_map.get(ensemble_prediction, "UNKNOWN")
        
        print(f"🎯 Ensemble Decision: {ensemble_signal} (prediction: {ensemble_prediction})")
        print(f"📊 Individual Predictions: {model_predictions}")
        print(f"📈 Vote Count: BUY({predictions.count(1)}) | SELL({predictions.count(-1)}) | HOLD({predictions.count(0)})")
        
        return ensemble_prediction
    
    def predict_with_details(self, features: List[float]) -> Dict:
        """
        Make prediction with detailed individual model votes.
        
        Args:
            features: List of 14 preprocessed features
            
        Returns:
            Dict: Contains ensemble prediction and individual model votes
        """
        if not self.models:
            print("❌ No models available for prediction")
            return {
                "ensemble_prediction": 0,
                "ensemble_signal": "HOLD",
                "model_votes": {},
                "vote_counts": {"BUY": 0, "SELL": 0, "HOLD": 0}
            }
        
        # Collect predictions from all models
        predictions = []
        model_predictions = {}
        
        for i, model in enumerate(self.models):
            model_name = self.model_names[i] if i < len(self.model_names) else f"Model_{i+1}"
            try:
                pred = model.predict([features])[0]
                predictions.append(pred)
                model_predictions[model_name] = pred
                
                # Map prediction to signal for logging
                signal_map = {1: "BUY", -1: "SELL", 0: "HOLD"}
                signal = signal_map.get(pred, "UNKNOWN")
                print(f"🎯 {model_name}: {signal} (prediction: {pred})")
                
            except Exception as e:
                print(f"❌ Prediction error in {model_name}: {e}")
                model_predictions[model_name] = 0  # Default to HOLD
        
        if not predictions:
            print("❌ No valid predictions from any model")
            return {
                "ensemble_prediction": 0,
                "ensemble_signal": "HOLD",
                "model_votes": {},
                "vote_counts": {"BUY": 0, "SELL": 0, "HOLD": 0}
            }
        
        # Majority voting: 1=BUY, -1=SELL, 0=HOLD
        ensemble_prediction = int(np.sign(np.sum(predictions)))
        
        # Log ensemble decision
        signal_map = {1: "BUY", -1: "SELL", 0: "HOLD"}
        ensemble_signal = signal_map.get(ensemble_prediction, "UNKNOWN")
        
        # Count votes
        vote_counts = {
            "BUY": predictions.count(1),
            "SELL": predictions.count(-1),
            "HOLD": predictions.count(0)
        }
        
        print(f"🎯 Ensemble Decision: {ensemble_signal} (prediction: {ensemble_prediction})")
        print(f"📊 Individual Predictions: {model_predictions}")
        print(f"📈 Vote Count: BUY({vote_counts['BUY']}) | SELL({vote_counts['SELL']}) | HOLD({vote_counts['HOLD']})")
        
        return {
            "ensemble_prediction": ensemble_prediction,
            "ensemble_signal": ensemble_signal,
            "model_votes": model_predictions,
            "vote_counts": vote_counts
        }
    
    def get_model_status(self) -> Dict[str, bool]:
        """Get status of all models in the ensemble."""
        return self.loaded_models.copy()
    
    def get_model_count(self) -> int:
        """Get number of successfully loaded models."""
        return len(self.models)
