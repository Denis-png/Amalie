from os import listdir, remove

for d in listdir('web'):
    try: 
        listdir(f'web/{d}')
        for s in listdir(f'web/{d}'):

            try:
                listdir(f'web/{d}/{s}')

                for f in listdir(f'web/{d}/{s}'):
                    try:
                        listdir(f'web/{d}/{s}/{f}')
                        for n in listdir(f'web/{d}/{s}/{f}'):
                            if 'Zone.Identifier' in n:
                                remove(f'web/{d}/{s}/{f}/{n}')
                    except:
                        continue
                    
            except:
                continue

    except:
        continue
