import shlex
import json
from catalog import Catalog
from photo import Photo

class FotologREPL:
    def __init__(self):
        self.cat = Catalog()

    def iniciar_repl(self):
        print("----- Fotolog REPL iniciado -----")
        print("Digite :help para ver os comandos ou :quit para sair.")

        while True:
            try:
                linha = input("> ").strip()
                if not linha: continue
                
                args = shlex.split(linha)
                cmd = args[0].lower()

                if cmd == ":quit":
                    print("Encerrando o Fotolog...")
                    break
                    
                elif cmd == ":help":
                    print("""
Lista de Comandos: 
:add <id> <ts> <path> [rating]               - Adiciona uma foto
:import <manifest.json>                      - Importar várias fotos
:range <ts1> <ts2>                           - Lista fotos com ts em [ts1, ts2]
:nearest <ts>                                - Foto com timestamp mais próximo.
:next <id>                                   - Mostra a próxima foto
:prev <id>                                   - Mostra a foto anterior
:get <id>                                    - Mostra os metadados de uma foto
:tag <id> <tag>                              - Anota uma tag a uma foto
:rate <id> <0 a 5>                           - Atribui rating a uma foto
:find-tag <tag>                              - Lista fotos com a tag (in-order).
:remove <id>                                 - Remove uma foto pelo id
:remove-range <ts1> <ts2>                    - Remove uma foto pelo intervalo de tempo
:stats                                       - Estatísticas
:list                                        - Listagem cronológica
:tree                                        - ASCII da árvore
:save <f>                                    - Salva o catálogo de fotos
:load <f>                                    - Carrega catálogo de fotos
:help                                        - Mostra os comandos disponíveis
:quit                                        - Encerra o programa

""")

                elif cmd == ":add":
                    id_foto = int(args[1])
                    ts = args[2]
                    path = args[3]
                    rating = int(args[4]) if len(args) > 4 else None
                    self.cat.add(Photo(id_foto, ts, path, rating=rating))
                    print(f"Foto {id_foto} adicionada com sucesso.")

                elif cmd == ":import":
                    caminho_arquivo = args[1]
                    sucesso = 0
                    ignorados = 0
                    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                        for d in dados:
                            try:
                                self.cat.add(Photo(d['id'], d['ts'], d['path'], d.get('tags', []), d.get('rating')))
                                sucesso += 1
                            except Exception:
                                ignorados += 1
                    print(f"Importação concluída. {sucesso} adicionadas, {ignorados} ignoradas.")

                elif cmd == ":range":
                    fotos = self.cat.range(args[1], args[2])
                    for f in fotos: 
                        print(f)
                    if not fotos:
                        print("Nenhuma foto encontrada neste intervalo.")

                elif cmd == ":nearest":
                    foto = self.cat.nearest(args[1])
                    print(foto if foto else "Catálogo vazio.")

                elif cmd == ":next":
                    foto = self.cat.next_of(int(args[1]))
                    print(foto if foto else "Nenhuma foto posterior encontrada.")

                elif cmd == ":prev":
                    foto = self.cat.prev_of(int(args[1]))
                    print(foto if foto else "Nenhuma foto anterior encontrada.")

                elif cmd == ":get":
                    foto = self.cat.get_by_id(int(args[1]))
                    print(f"ID: {foto._id} | TS: {foto._timestamp} | Path: {foto._path} | Tags: {foto._tags} | Rating: {foto._rating}")

                elif cmd == ":tag":
                    id_foto = int(args[1])
                    tag = args[2]
                    self.cat.tag(id_foto, tag)
                    print(f"Tag '{tag}' adicionada à foto {id_foto}.")

                elif cmd == ":rate":
                    id_foto = int(args[1])
                    nota = int(args[2])
                    self.cat.rate(id_foto, nota)
                    print(f"Nota {nota} atribuída à foto {id_foto}.")

                elif cmd == ":find-tag":
                    fotos = self.cat.find_by_tag(args[1])
                    for f in fotos: 
                        print(f)
                    if not fotos:
                        print(f"Nenhuma foto encontrada com a tag '{args[1]}'.")

                elif cmd == ":remove":
                    self.cat.remove(int(args[1]))
                    print(f"Foto {args[1]} removida com sucesso.")

                elif cmd == ":remove-range":
                    qtd = self.cat.remove_range(args[1], args[2])
                    print(f"{qtd} foto(s) removida(s) no intervalo.")

                elif cmd == ":stats":
                    estatisticas = self.cat.stats()
                    if isinstance(estatisticas, dict):
                        for chave, valor in estatisticas.items():
                            print(f"{chave}: {valor}")
                    else:
                        print(estatisticas)

                elif cmd == ":list":
                    print(self.cat)

                elif cmd == ":tree":
                    self.cat._index.print_binary_tree()

                elif cmd == ":save":
                    self.cat.save(args[1])
                    print(f"Catálogo salvo em {args[1]}.")

                elif cmd == ":load":
                    self.cat.load(args[1])
                    print(f"Catálogo carregado de {args[1]}.")

                else:
                    print("Comando desconhecido. Digite :help para ver a lista de comandos.")
                    
            except IndexError:
                print("Erro: Argumentos insuficientes para este comando. Digite :help para verificar a sintaxe.")
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Erro inesperado: {e}")

