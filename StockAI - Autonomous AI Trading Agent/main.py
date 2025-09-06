# main.py
import time
import json
from datetime import datetime, timedelta
from agents.data_fetcher import get_stock_data
from agents.decision_engine import create_decision_engine
from agents.execution_agent import ExecutionAgent
from utils.config import STOCK_LIST

def main():
    print("🚀 Starting StockAI - Advanced Multi-Agent Trading System...")
    print("=" * 60)
    
    # Initialize decision engine and execution agent
    decision_engine = create_decision_engine()
    exec_agent = ExecutionAgent()

    # Initialize portfolio
    portfolio = {
        "cash": 100000,  # Starting cash
        "positions": {},  # Current positions
        "cost_basis": {}  # Cost basis for each position
    }

    # Set date range for analysis (last 30 days)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    print(f"📊 Portfolio initialized with ${portfolio['cash']:,}")
    print(f"📅 Analysis period: {start_date} to {end_date}")
    print(f"🎯 Monitoring {len(STOCK_LIST)} stocks: {', '.join(STOCK_LIST)}")
    print("=" * 60)

    cycle_count = 0
    
    while True:
        cycle_count += 1
        print(f"\n🔄 === CYCLE #{cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        
        cycle_results = {
            "cycle": cycle_count,
            "timestamp": datetime.now().isoformat(),
            "stocks_analyzed": [],
            "decisions_made": 0,
            "trades_executed": 0,
            "errors": []
        }

        for stock in STOCK_LIST:
            print(f"\n📈 Analyzing {stock}...")
            
            try:
                # Fetch historical/real-time stock data
                stock_data = get_stock_data(stock)
                if stock_data is None:
                    print(f"❌ Failed to fetch data for {stock}")
                    cycle_results["errors"].append(f"Data fetch failed for {stock}")
                    continue

                # Run comprehensive analysis using decision engine
                analysis_result = decision_engine.run_comprehensive_analysis(
                    stock, stock_data, start_date, end_date, portfolio
                )
                
                if "error" in analysis_result:
                    print(f"❌ Analysis failed for {stock}: {analysis_result['error']}")
                    cycle_results["errors"].append(f"Analysis failed for {stock}: {analysis_result['error']}")
                    continue

                # Extract final decision
                final_decision = analysis_result["final_decision"]
                trade_signal = final_decision["signal"]
                confidence = final_decision["confidence"]
                quantity = final_decision["quantity"]
                agent_consensus = final_decision["agent_consensus"]
                agent_signal_counts = final_decision["agent_signal_counts"]
                rl_decision = final_decision["rl_decision"]
                
                print(f"🎯 Final Decision: {trade_signal}")
                print(f"📊 Confidence: {confidence}%")
                print(f"📦 Quantity: {quantity} shares")
                print(f"📈 Agent Consensus: {agent_consensus}")
                print(f"📊 Agent Signals: {agent_signal_counts}")
                print(f"🤖 RL Decision: {rl_decision['signal']} ({rl_decision['confidence']}%)")
                print(f"💭 Reasoning: {final_decision['reasoning']}")
                
                # Store analysis results
                stock_result = {
                    "stock": stock,
                    "signal": trade_signal,
                    "confidence": confidence,
                    "quantity": quantity,
                    "agent_consensus": agent_consensus,
                    "agent_signal_counts": agent_signal_counts,
                    "rl_decision": rl_decision,
                    "reasoning": final_decision["reasoning"]
                }
                cycle_results["stocks_analyzed"].append(stock_result)
                cycle_results["decisions_made"] += 1

                # Execute trade based on the generated signal and quantity
                if trade_signal in ["BUY", "SELL"] and confidence > 60 and quantity > 0:  # Only trade with high confidence and positive quantity
                    try:
                        exec_agent.execute_trade(stock, trade_signal, quantity)
                        print(f"✅ Trade execution completed for {stock}: {trade_signal} {quantity} shares")
                        cycle_results["trades_executed"] += 1
                    except Exception as e:
                        print(f"❌ Trade execution failed for {stock}: {e}")
                        cycle_results["errors"].append(f"Trade execution failed for {stock}: {e}")
                else:
                    if quantity == 0:
                        print(f"⏸️  Holding {stock} (quantity: 0)")
                    else:
                        print(f"⏸️  Holding {stock} (confidence: {confidence}%, quantity: {quantity})")
                    
            except Exception as e:
                print(f"❌ Unexpected error analyzing {stock}: {e}")
                cycle_results["errors"].append(f"Unexpected error for {stock}: {e}")

        # Print cycle summary
        print(f"\n📋 === CYCLE #{cycle_count} SUMMARY ===")
        print(f"📊 Stocks Analyzed: {len(cycle_results['stocks_analyzed'])}")
        print(f"🎯 Decisions Made: {cycle_results['decisions_made']}")
        print(f"💼 Trades Executed: {cycle_results['trades_executed']}")
        print(f"❌ Errors: {len(cycle_results['errors'])}")
        
        # Show signal distribution
        signals = [s["signal"] for s in cycle_results["stocks_analyzed"]]
        if signals:
            buy_count = signals.count("BUY")
            sell_count = signals.count("SELL")
            hold_count = signals.count("HOLD")
            print(f"📈 Signal Distribution: BUY({buy_count}) | SELL({sell_count}) | HOLD({hold_count})")
        
        # Show performance summary every 10 cycles
        if cycle_count % 10 == 0:
            print(f"\n📊 === PERFORMANCE SUMMARY (Last 10 Cycles) ===")
            performance = decision_engine.get_performance_summary()
            print(f"🎯 Total Decisions: {performance.get('total_decisions', 0)}")
            print(f"📊 Average Confidence: {performance.get('average_confidence', 0):.1f}%")
            
            signal_dist = performance.get('signal_distribution', {})
            print(f"📈 Signal Distribution: BUY({signal_dist.get('BUY', 0)}) | SELL({signal_dist.get('SELL', 0)}) | HOLD({signal_dist.get('HOLD', 0)})")

        print(f"\n⏰ Waiting 60 seconds for next cycle...")
        time.sleep(60)  # Delay between cycles (60 seconds)

if __name__ == "__main__":
    main()
