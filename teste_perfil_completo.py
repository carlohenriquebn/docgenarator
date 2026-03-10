"""
Teste com payload COMPLETO - verifica se o LLM usa as informações
"""
import requests
import json


def teste_com_perfil_completo():
    """Teste com todas as informações do perfil"""
    print("="*80)
    print("🧪 TESTE COM PERFIL COMPLETO")
    print("="*80)
    print("\n💡 Testando se o LLM usa as informações fornecidas\n")
    
    # Payload COMPLETO com todas as informações
    payload = {
        "profile": {
            "idade": 28,
            "cidade": "São Paulo",
            "estado": "SP",
            "modelo_carro": "Honda Civic",
            "ano_carro": 2022,
            "valor_carro": 120000.0,
            "historico_sinistros": 0,
            "uso_veiculo": "particular",
            "cobertura_desejada": "compreensiva",
            "mensagem": "Quero as 3 melhores seguradoras considerando bom custo-benefício"
        },
        "search_type": "recursive",
        "max_iterations": 3,
        "quality_threshold": 8.0,
        "enable_logging": True,
        "log_level": "INFO"
    }
    
    print("📋 PERFIL FORNECIDO:")
    print(f"   ✅ Idade: {payload['profile']['idade']} anos")
    print(f"   ✅ Localização: {payload['profile']['cidade']}, {payload['profile']['estado']}")
    print(f"   ✅ Veículo: {payload['profile']['modelo_carro']} {payload['profile']['ano_carro']}")
    print(f"   ✅ Valor: R$ {payload['profile']['valor_carro']:,.2f}")
    print(f"   ✅ Sinistros: {payload['profile']['historico_sinistros']}")
    print(f"   ✅ Uso: {payload['profile']['uso_veiculo']}")
    print(f"   ✅ Cobertura: {payload['profile']['cobertura_desejada']}")
    
    print("\n🚀 Enviando para API...\n")
    
    try:
        # Verifica se API está online
        requests.get("http://localhost:3000/", timeout=2)
    except:
        print("❌ API não está rodando!")
        print("   Execute: py main.py\n")
        return
    
    try:
        response = requests.post(
            "http://localhost:3000/chat/insurance/recursive",
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"❌ Erro HTTP {response.status_code}")
            print(f"Detalhes: {response.json()}")
            return
        
        result = response.json()
        
        print("="*80)
        print("✅ RESULTADO")
        print("="*80)
        
        # Exibe métricas
        print(f"\n📊 MÉTRICAS:")
        print(f"   Score: {result.get('quality_score', 'N/A'):.1f}/10")
        print(f"   Iterações: {result.get('total_iterations', 'N/A')}")
        print(f"   Convergiu: {'Sim ✅' if result.get('converged', False) else 'Não ❌'}")
        
        # Análise da resposta
        response_text = result.get('response', '')
        
        print(f"\n🔍 ANÁLISE DA RESPOSTA:")
        
        # Verifica se usou as informações
        checks = {
            "Mencionou idade (28)": "28" in response_text,
            "Mencionou São Paulo": "São Paulo" in response_text or "SP" in response_text,
            "Mencionou Honda Civic": "Honda Civic" in response_text or "Civic" in response_text,
            "Mencionou valor (120000)": "120" in response_text or "120.000" in response_text,
            "Mencionou sem sinistros": "sem sinistro" in response_text.lower() or "nenhum sinistro" in response_text.lower() or "0 sinistro" in response_text.lower(),
            "NÃO pediu informações": "preciso que você" not in response_text.lower() and "forneça" not in response_text.lower() and "compartilhe" not in response_text.lower()
        }
        
        passed = sum(checks.values())
        total = len(checks)
        
        for check, status in checks.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {check}")
        
        print(f"\n📈 Aproveitamento: {passed}/{total} ({passed/total*100:.0f}%)")
        
        # Verifica histórico de iterações
        if result.get('iterations'):
            print(f"\n📋 HISTÓRICO DE SCORES:")
            for it in result['iterations']:
                score = it.get('quality_score', 0)
                icon = "🏆" if score >= 8 else "⚠️" if score >= 6 else "❌"
                print(f"   {icon} Iteração {it['iteration']}: {score:.1f}/10")
        
        # Exibe resposta final
        print(f"\n💬 RESPOSTA FINAL:")
        print("-"*80)
        print(response_text[:500])
        if len(response_text) > 500:
            print(f"... (+ {len(response_text)-500} caracteres)")
        print("-"*80)
        
        # Recomendações
        print(f"\n💡 RECOMENDAÇÕES:")
        if result.get('quality_score', 0) < 7:
            print("   ⚠️  Score baixo - considere ajustar o prompt")
            print("   📝 Verifique os logs para detalhes")
        elif not result.get('converged', False):
            print("   ⚠️  Não convergiu - considere aumentar max_iterations")
        else:
            print("   ✅ Excelente! Sistema funcionando bem")
        
        print(f"\n📁 Logs detalhados em: recursive_search.log")
        
    except requests.exceptions.Timeout:
        print("❌ Timeout - requisição demorou muito")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def teste_sem_perfil():
    """Teste SEM perfil para comparar"""
    print("\n" + "="*80)
    print("🧪 TESTE SEM PERFIL (para comparação)")
    print("="*80)
    print("\n💡 Veja a diferença quando não fornecemos informações\n")
    
    payload = {
        "profile": {
            "mensagem": "Quais as melhores seguradoras?"
        },
        "search_type": "recursive",
        "max_iterations": 2,
        "enable_logging": False
    }
    
    try:
        response = requests.post(
            "http://localhost:3000/chat/insurance/recursive",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"📊 Score: {result.get('quality_score', 'N/A'):.1f}/10")
            print(f"\n💬 Resposta (primeiras linhas):")
            print("-"*80)
            print(result.get('response', '')[:300])
            print("...")
            print("-"*80)
            print("\n💡 Note: Sem perfil, o LLM provavelmente pede informações\n")
        
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║      🧪 TESTE DE VALIDAÇÃO - PERFIL COMPLETO 🧪                          ║
║                                                                           ║
║  Verifica se o LLM está usando as informações fornecidas                 ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")
    
    teste_com_perfil_completo()
    
    continuar = input("\n\nDeseja testar SEM perfil para comparar? (s/n): ")
    if continuar.lower() == 's':
        teste_sem_perfil()
    
    print("\n✅ Testes concluídos!\n")
