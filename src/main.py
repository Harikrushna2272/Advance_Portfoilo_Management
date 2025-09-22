# Main application entry point for StockAI
import asyncio
import signal
import sys
from datetime import datetime, timedelta
from typing import Dict, Any

from src.config.settings import get_settings
from src.utils.logger import setup_logger
from src.core.decision_engine import DecisionEngine
from src.agents.execution_agent import ExecutionAgent
from src.utils.validators import validate_stock_list

# Global variables for graceful shutdown
shutdown_event = asyncio.Event()
logger = setup_logger("stockai.main")


class StockAIApplication:
    """Main StockAI application class."""
    
    def __init__(self):
        """Initialize the StockAI application."""
        self.settings = get_settings()
        self.decision_engine = None
        self.execution_agent = None
        self.portfolio = {
            "cash": self.settings.initial_cash,
            "positions": {},
            "cost_basis": {}
        }
        self.cycle_count = 0
        
        # Validate configuration
        self._validate_configuration()
        
        logger.info("StockAI application initialized")
    
    def _validate_configuration(self):
        """Validate application configuration."""
        if not validate_stock_list(self.settings.stock_list):
            raise ValueError("Invalid stock list configuration")
        
        if not self.settings.api_key or not self.settings.api_secret:
            raise ValueError("Alpaca API credentials not configured")
        
        logger.info("Configuration validated successfully")
    
    async def initialize_services(self):
        """Initialize all services."""
        try:
            logger.info("Initializing services...")
            
            # Initialize decision engine
            self.decision_engine = DecisionEngine()
            await self.decision_engine.initialize()
            
            # Initialize execution agent
            self.execution_agent = ExecutionAgent()
            await self.execution_agent.initialize()
            
            logger.info("All services initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            raise
    
    async def run_trading_cycle(self):
        """Run a single trading cycle."""
        self.cycle_count += 1
        cycle_start = datetime.now()
        
        logger.info(f"🔄 Starting trading cycle #{self.cycle_count}")
        
        cycle_results = {
            "cycle": self.cycle_count,
            "timestamp": cycle_start.isoformat(),
            "stocks_analyzed": [],
            "decisions_made": 0,
            "trades_executed": 0,
            "errors": []
        }
        
        # Set date range for analysis
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        for stock in self.settings.stock_list:
            try:
                logger.info(f"📈 Analyzing {stock}...")
                
                # Run comprehensive analysis
                analysis_result = await self.decision_engine.run_comprehensive_analysis(
                    stock=stock,
                    start_date=start_date,
                    end_date=end_date,
                    portfolio=self.portfolio
                )
                
                if "error" in analysis_result:
                    logger.error(f"Analysis failed for {stock}: {analysis_result['error']}")
                    cycle_results["errors"].append(f"Analysis failed for {stock}: {analysis_result['error']}")
                    continue
                
                # Extract final decision
                final_decision = analysis_result["final_decision"]
                trade_signal = final_decision["signal"]
                confidence = final_decision["confidence"]
                quantity = final_decision["quantity"]
                
                logger.info(f"🎯 Decision for {stock}: {trade_signal} (confidence: {confidence}%, quantity: {quantity})")
                
                # Store analysis results
                stock_result = {
                    "stock": stock,
                    "signal": trade_signal,
                    "confidence": confidence,
                    "quantity": quantity,
                    "agent_consensus": final_decision.get("agent_consensus", "unknown"),
                    "rl_decision": final_decision.get("rl_decision", {}),
                    "reasoning": final_decision.get("reasoning", "")
                }
                cycle_results["stocks_analyzed"].append(stock_result)
                cycle_results["decisions_made"] += 1
                
                # Execute trade if conditions are met
                if (trade_signal in ["BUY", "SELL"] and 
                    confidence > self.settings.confidence_threshold and 
                    quantity > 0):
                    
                    try:
                        await self.execution_agent.execute_trade(
                            symbol=stock,
                            action=trade_signal,
                            quantity=quantity
                        )
                        logger.info(f"✅ Trade executed for {stock}: {trade_signal} {quantity} shares")
                        cycle_results["trades_executed"] += 1
                        
                    except Exception as e:
                        logger.error(f"Trade execution failed for {stock}: {e}")
                        cycle_results["errors"].append(f"Trade execution failed for {stock}: {e}")
                else:
                    logger.info(f"⏸️  Holding {stock} (confidence: {confidence}%, quantity: {quantity})")
                    
            except Exception as e:
                logger.error(f"Unexpected error analyzing {stock}: {e}")
                cycle_results["errors"].append(f"Unexpected error for {stock}: {e}")
        
        # Log cycle summary
        cycle_duration = (datetime.now() - cycle_start).total_seconds()
        self._log_cycle_summary(cycle_results, cycle_duration)
        
        # Log performance summary every 10 cycles
        if self.cycle_count % 10 == 0:
            await self._log_performance_summary()
    
    def _log_cycle_summary(self, cycle_results: Dict[str, Any], duration: float):
        """Log cycle summary."""
        logger.info(f"📋 Cycle #{self.cycle_count} Summary:")
        logger.info(f"   📊 Stocks Analyzed: {len(cycle_results['stocks_analyzed'])}")
        logger.info(f"   🎯 Decisions Made: {cycle_results['decisions_made']}")
        logger.info(f"   💼 Trades Executed: {cycle_results['trades_executed']}")
        logger.info(f"   ❌ Errors: {len(cycle_results['errors'])}")
        logger.info(f"   ⏱️  Duration: {duration:.2f}s")
        
        # Show signal distribution
        signals = [s["signal"] for s in cycle_results["stocks_analyzed"]]
        if signals:
            buy_count = signals.count("BUY")
            sell_count = signals.count("SELL")
            hold_count = signals.count("HOLD")
            logger.info(f"   📈 Signal Distribution: BUY({buy_count}) | SELL({sell_count}) | HOLD({hold_count})")
    
    async def _log_performance_summary(self):
        """Log performance summary."""
        logger.info(f"📊 Performance Summary (Last 10 Cycles):")
        
        if self.decision_engine:
            performance = self.decision_engine.get_performance_summary()
            logger.info(f"   🎯 Total Decisions: {performance.get('total_decisions', 0)}")
            logger.info(f"   📊 Average Confidence: {performance.get('average_confidence', 0):.1f}%")
            
            signal_dist = performance.get('signal_distribution', {})
            logger.info(f"   📈 Signal Distribution: BUY({signal_dist.get('BUY', 0)}) | SELL({signal_dist.get('SELL', 0)}) | HOLD({signal_dist.get('HOLD', 0)})")
    
    async def run(self):
        """Main application loop."""
        try:
            logger.info("🚀 Starting StockAI Trading System...")
            logger.info(f"📊 Portfolio initialized with ${self.portfolio['cash']:,}")
            logger.info(f"🎯 Monitoring {len(self.settings.stock_list)} stocks: {', '.join(self.settings.stock_list)}")
            
            # Initialize services
            await self.initialize_services()
            
            # Main trading loop
            while not shutdown_event.is_set():
                try:
                    await self.run_trading_cycle()
                    
                    # Wait for next cycle
                    logger.info(f"⏰ Waiting {self.settings.cycle_interval} seconds for next cycle...")
                    await asyncio.wait_for(
                        shutdown_event.wait(), 
                        timeout=self.settings.cycle_interval
                    )
                    
                except asyncio.TimeoutError:
                    # Normal timeout, continue to next cycle
                    continue
                except Exception as e:
                    logger.error(f"Error in trading cycle: {e}")
                    await asyncio.sleep(5)  # Wait before retrying
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}")
            raise
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Graceful shutdown."""
        logger.info("🛑 Shutting down StockAI...")
        
        if self.decision_engine:
            await self.decision_engine.shutdown()
        
        if self.execution_agent:
            await self.execution_agent.shutdown()
        
        logger.info("✅ StockAI shutdown complete")


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}")
    shutdown_event.set()


async def main():
    """Main entry point."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run application
    app = StockAIApplication()
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)
