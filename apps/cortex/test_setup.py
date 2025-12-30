from core.llm_factory import LLMFactory

def test_the_stack():
    print("--- NexusStudio: Infrastructure Test ---")
    
    # 1. Test The Brain
    print(f"\n🧠 Testing Brain [{LLMFactory.get_brain().model_name}]...")
    try:
        brain = LLMFactory.get_brain()
        response = brain.invoke("Explain Quantum Computing in one sentence.")
        print(f"✅ Success: {response.content}")
    except Exception as e:
        print(f"❌ Brain Failed: {e}")

    # 2. Test The Reflex
    print(f"\n⚡ Testing Reflex [{LLMFactory.get_reflex().model_name}]...")
    try:
        reflex = LLMFactory.get_reflex()
        response = reflex.invoke("What is 2+2? Only output the number.")
        print(f"✅ Success: {response.content}")
    except Exception as e:
        print(f"❌ Reflex Failed: {e}")

if __name__ == "__main__":
    test_the_stack()