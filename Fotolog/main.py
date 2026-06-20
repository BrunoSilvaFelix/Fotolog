from repl import FotologREPL

if __name__ == "__main__":
    app = FotologREPL()
    
    try:
        app.iniciar_repl()
    except KeyboardInterrupt:
        print("\n\nEncerrando o Fotolog...")