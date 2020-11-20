Proyecto Base de Datos Dinamica Distribuida para Sistema Operativo 2

Este programa es una version multi threaded utilizando servidor tradicional de socket y servidor select de socket para simular una base de datos distribuida. Como fue solicitado se asume que las nodos seran ejecutados previo a la utilizacion e invocacion de llamadas RPC.

Cada nodo local intentara replicar hacia los demas nodos cualquier nuevas llamadas RPC realizada desde la app local al nodo.

De igual manera cada nodo replicara toda invocacion RPC de otro nodo si esta no ha sido realizada antes.

Se utiliza un historial para conocer las invocaciones realizadas/replicadas. Este historial tambien sirve para reducir la cantidad de mensajes a enviar omitiendo en las replicas el origen y que nodo envio la RPC.

Los nodos pueden recibir libremente las replicas pero de haber sido ya procesadas seran ignoradas, y se enviaran todos los mensajes posible y disponibles hasta vaciar la cola.

Probado usando python 3.8.6.

En Windows usar interpretador de venv:
```console
    venv\Scripts\activate
```  

Comando en Windows ejecutar server script:
```console
    python dstore_main.py
```

Modificar los parametros que se mencionan en el script cliente
```console
    python app_client.py
```

Cada proceso/servidor/nodo imprimira en pantalla los mensajes que seran enviados y a quien, al igual que las invocaciones estan programadas a realizarse recibidas desde otros nodos y cual nodo.


