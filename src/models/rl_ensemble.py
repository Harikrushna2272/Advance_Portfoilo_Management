"""
RL Ensemble Model System

Loads and manages 5 trained RL models for trading decisions:
- SAC (Soft Actor-Critic)
- PPO (Proximal Policy Optimization)
- A2C (Advantage Actor-Critic)
- TD3 (Twin Delayed Deep Deterministic)
- DDPG (Deep Deterministic Policy Gradient)

Models are trained using Stable-Baselines3 on historical stock data.
"""

import os
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Stable-Baselines3 imports
try:
    from stable_baselines3 import SAC, PPO, A2C, TD3, DDPG

    SB3_AVAILABLE = True
except ImportError:
    SB3_AVAILABLE = False
    logging.warning("Stable-Baselines3 not installed. RL models will not be available.")

logger = logging.getLogger(__name__)


class RLEnsemble:
    """
    Ensemble of 5 RL models for robust trading predictions.

    Uses majority voting to combine predictions from multiple algorithms.
    """

    def __init__(self, models_dir: Optional[str] = None):
        """
        Initialize RL Ensemble.

        Args:
            models_dir: Directory containing trained model zip files
        """
        if not SB3_AVAILABLE:
            raise ImportError(
                "Stable-Baselines3 is required for RL models. Install with: pip install stable-baselines3"
            )

        # Set models directory
        if models_dir is None:
            # Default to project models directory
            project_root = Path(__file__).parent.parent.parent
            self.models_dir = project_root / "models"
        else:
            self.models_dir = Path(models_dir)

        # Model configurations
        self.model_configs = {
            "SAC": {"class": SAC, "file": "agent_sac.zip"},
            "PPO": {"class": PPO, "file": "agent_ppo.zip"},
            "A2C": {"class": A2C, "file": "agent_a2c.zip"},
            "TD3": {"class": TD3, "file": "agent_td3.zip"},
            "DDPG": {"class": DDPG, "file": "agent_ddpg.zip"},
        }

        # Loaded models
        self.models: Dict[str, any] = {}
        self.model_status: Dict[str, bool] = {}

        # Load all models
        self._load_all_models()

    def _load_all_models(self):
        """Load all RL models from disk."""
        logger.info(f"🤖 Loading RL Ensemble from {self.models_dir}")

        for name, config in self.model_configs.items():
            model_path = self.models_dir / config["file"]

            if not model_path.exists():
                logger.warning(f"⚠️  {name} model not found at {model_path}")
                self.model_status[name] = False
                continue

            try:
                # Load model using Stable-Baselines3
                model_class = config["class"]
                model = model_class.load(str(model_path))

                self.models[name] = model
                self.model_status[name] = True
                logger.info(f"✅ {name} loaded successfully")

            except Exception as e:
                logger.error(f"❌ Failed to load {name}: {e}")
                self.model_status[name] = False

        loaded_count = sum(self.model_status.values())
        total_count = len(self.model_configs)
        logger.info(f"📊 Ensemble Status: {loaded_count}/{total_count} models loaded")

        if loaded_count == 0:
            logger.error("❌ No RL models loaded! Ensemble will not function.")

    def predict(
        self, observation: np.ndarray, deterministic: bool = True
    ) -> Tuple[int, Dict]:
        """
        Make prediction using ensemble of RL models.

        Args:
            observation: Numpy array of features (shape: (n_features,))
            deterministic: Use deterministic actions (recommended for inference)

        Returns:
            Tuple of (ensemble_action, details_dict)
            - ensemble_action: 0=HOLD, 1=BUY, 2=SELL (or continuous value)
            - details_dict: Individual model predictions and voting details
        """
        if not self.models:
            logger.warning("⚠️  No models available for prediction")
            return 0, {"error": "No models loaded"}

        # Collect predictions from all models
        predictions = []
        model_predictions = {}

        for name, model in self.models.items():
            try:
                # Predict action from model
                action, _ = model.predict(observation, deterministic=deterministic)

                # Convert action to discrete signal if needed
                # Most models output continuous values or discrete actions
                if isinstance(action, np.ndarray):
                    action = action.item() if action.size == 1 else action[0]

                predictions.append(action)
                model_predictions[name] = float(action)

                logger.debug(f"{name} prediction: {action}")

            except Exception as e:
                logger.error(f"❌ Prediction error in {name}: {e}")
                model_predictions[name] = 0  # Default to HOLD/neutral

        if not predictions:
            logger.warning("❌ No valid predictions from any model")
            return 0, {"error": "All model predictions failed"}

        # Ensemble strategy: Majority voting or averaging
        # For continuous actions, average them
        # For discrete actions, use majority vote
        ensemble_action = np.mean(predictions)

        # Convert to discrete action (0=HOLD, 1=BUY, 2=SELL)
        # This mapping depends on your environment's action space
        # Adjust thresholds as needed
        if ensemble_action > 0.5:
            discrete_action = 1  # BUY
            signal = "BUY"
        elif ensemble_action < -0.5:
            discrete_action = 2  # SELL
            signal = "SELL"
        else:
            discrete_action = 0  # HOLD
            signal = "HOLD"

        # Calculate confidence based on agreement
        if predictions:
            std = np.std(predictions)
            confidence = max(
                0, min(100, 100 * (1 - std))
            )  # Higher agreement = higher confidence
        else:
            confidence = 0

        details = {
            "ensemble_action": float(ensemble_action),
            "discrete_action": discrete_action,
            "signal": signal,
            "confidence": confidence,
            "model_predictions": model_predictions,
            "num_models": len(predictions),
            "prediction_std": float(np.std(predictions)) if predictions else 0,
        }

        logger.info(f"🎯 Ensemble Decision: {signal} (confidence: {confidence:.1f}%)")
        logger.debug(f"Model predictions: {model_predictions}")

        return discrete_action, details

    def predict_with_details(self, observation: np.ndarray) -> Dict:
        """
        Make prediction and return detailed breakdown.

        Args:
            observation: Numpy array of features

        Returns:
            Dictionary with ensemble prediction and all model details
        """
        action, details = self.predict(observation, deterministic=True)

        # Add action mapping
        action_map = {0: "HOLD", 1: "BUY", 2: "SELL"}
        details["action_name"] = action_map.get(action, "UNKNOWN")
        details["action_code"] = action

        return details

    def get_model_status(self) -> Dict[str, bool]:
        """Get loading status of all models."""
        return self.model_status.copy()

    def get_loaded_models(self) -> List[str]:
        """Get list of successfully loaded models."""
        return [name for name, status in self.model_status.items() if status]

    def is_ready(self) -> bool:
        """Check if ensemble has at least one model loaded."""
        return len(self.models) > 0


def create_rl_ensemble(models_dir: Optional[str] = None) -> RLEnsemble:
    """
    Create and return an RL Ensemble instance.

    Args:
        models_dir: Directory containing trained models

    Returns:
        RLEnsemble instance
    """
    return RLEnsemble(models_dir=models_dir)


# Backwards compatibility with old EnsembleRLModel
class EnsembleRLModel:
    """
    Legacy wrapper for backwards compatibility.
    Maps old interface to new RLEnsemble.
    """

    def __init__(self, model_paths: List[str]):
        """
        Initialize using list of model paths.

        Args:
            model_paths: List of paths to model zip files
        """
        logger.warning("EnsembleRLModel is deprecated. Use RLEnsemble instead.")

        # Extract directory from first path
        if model_paths:
            models_dir = Path(model_paths[0]).parent
        else:
            models_dir = None

        self.ensemble = RLEnsemble(models_dir=models_dir)
        self.models = self.ensemble.models
        self.loaded_models = self.ensemble.model_status

    def predict(self, features: List[float]) -> int:
        """Make prediction (legacy interface)."""
        observation = np.array(features, dtype=np.float32)
        action, _ = self.ensemble.predict(observation)

        # Map discrete action to legacy format: 1=BUY, -1=SELL, 0=HOLD
        action_map = {0: 0, 1: 1, 2: -1}
        return action_map.get(action, 0)

    def predict_with_details(self, features: List[float]) -> Dict:
        """Make prediction with details (legacy interface)."""
        observation = np.array(features, dtype=np.float32)
        details = self.ensemble.predict_with_details(observation)

        # Map to legacy format
        action = details["action_code"]
        action_map = {0: 0, 1: 1, 2: -1}
        legacy_prediction = action_map.get(action, 0)

        signal_map = {1: "BUY", -1: "SELL", 0: "HOLD"}

        return {
            "ensemble_prediction": legacy_prediction,
            "ensemble_signal": signal_map[legacy_prediction],
            "model_votes": details["model_predictions"],
            "vote_counts": self._count_votes(details["model_predictions"]),
        }

    def _count_votes(self, predictions: Dict[str, float]) -> Dict[str, int]:
        """Count votes from model predictions."""
        counts = {"BUY": 0, "SELL": 0, "HOLD": 0}

        for pred in predictions.values():
            if pred > 0.5:
                counts["BUY"] += 1
            elif pred < -0.5:
                counts["SELL"] += 1
            else:
                counts["HOLD"] += 1

        return counts

    def get_model_status(self) -> Dict[str, bool]:
        """Get model status."""
        return self.ensemble.get_model_status()

    def get_model_count(self) -> int:
        """Get number of loaded models."""
        return len(self.ensemble.models)


if __name__ == "__main__":
    # Test RL Ensemble
    logging.basicConfig(level=logging.INFO)

    try:
        # Create ensemble
        ensemble = create_rl_ensemble()

        # Check status
        print(f"\nLoaded models: {ensemble.get_loaded_models()}")
        print(f"Ensemble ready: {ensemble.is_ready()}")

        # Test prediction with dummy data
        if ensemble.is_ready():
            # Create dummy observation (14 features)
            dummy_obs = np.random.randn(14).astype(np.float32)

            # Make prediction
            action, details = ensemble.predict(dummy_obs)
            print(f"\nTest Prediction:")
            print(f"Action: {action}")
            print(f"Signal: {details['signal']}")
            print(f"Confidence: {details['confidence']:.1f}%")
            print(f"Model predictions: {details['model_predictions']}")

    except Exception as e:
        print(f"Error testing RL Ensemble: {e}")
