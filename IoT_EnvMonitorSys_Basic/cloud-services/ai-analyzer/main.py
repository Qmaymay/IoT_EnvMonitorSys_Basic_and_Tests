# 在 main.py 中使用
from ai_analyzer.real_ai_analyzer import RealAIAnalyzer

# 初始化真正的AI分析器
ai_analyzer = RealAIAnalyzer()

# 使用AI分析数据
result = ai_analyzer.analyze_with_ai("device_001", 28.5, 65.0, 85.0)

print("🤖 AI分析结果:")
print(f"   环境类型: {result['environment_type']}")
print(f"   预测置信度: {result['prediction_confidence']}")
print(f"   异常分数: {result['anomaly_score']}")
print(f"   AI建议: {result['ai_suggestions']}")