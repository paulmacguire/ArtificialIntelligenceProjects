% Esta línea define el dominio de tiempo en el que se llevarán a cabo los movimientos.
% 'bound' es un número arbitrario que representa el límite superior del intervalo de tiempo.
tiempo(0..bound).
#const numero_brazo = 1.

% Definición de los lugares donde se pueden colocar los bloques.
lugar(X) :- bloque(X).
lugar(mesa).

% Esta línea define la acción de ejecutar un movimiento. En cada instante de tiempo T,
% se puede ejecutar un movimiento posible de un bloque X a un lugar Y, siempre que T
% sea diferente de 'bound'. Con la restricción de cardinalidad se asegura que no se
% ejecuten más de un movimiento en cada instante de tiempo.
0{ejecutar(X,Y,T) : movimientoposible(X,Y,T)}numero_brazo :- tiempo(T), T!=bound.

% Estas líneas definen los bloques que están siendo movidos en un instante de tiempo T y sus destinos.
origen_movimiento(X,T) :- ejecutar(X,Y,T).
destino_movimiento(Y,T) :- ejecutar(X,Y,T).

% Esta línea indica que un bloque X sigue estando sobre el bloque Y en el tiempo T+1
% si no está siendo movido en el tiempo T. En otras palabras, si no se origina un
% movimiento de X en T, X seguirá sobre Y en T+1.
sobre(X,Y,T+1) :-
	tiempo(T),
	sobre(X,Y,T),
	not origen_movimiento(X,T).

% Esta línea indica que un bloque X estará sobre el bloque Y en el tiempo T+1
% si se ejecuta un movimiento desde X a Y en el tiempo T.
sobre(X,Y,T+1) :-
	bloque(X),lugar(Y),tiempo(T),
	ejecutar(X,Y,T).

% Estas líneas definen si un bloque está tapado (tiene otro bloque encima) o
% libre en un instante de tiempo T. Si X está sobre Y en el tiempo T, Y está tapado por X.
% Si X no está tapado por ningún bloque en el tiempo T, entonces X está libre.
bloquetapado(Y,T) :- sobre(X,Y,T), tiempo(T).
bloquelibre(X,T) :- bloque(X), tiempo(T), not bloquetapado(X,T).

% Estas líneas definen las condiciones para que un movimiento sea posible. Un bloque X puede
% moverse a un bloque Y si ambos bloques están libres y X no está ya sobre Y en el instante
% de tiempo T. Además, X no puede moverse y quedar sobre sí mismo (X!=Y).
movimientoposible(X,Y,T) :- bloquelibre(X,T), bloquelibre(Y,T), X!=Y, not sobre(X,Y,T).
% Un bloque X también puede moverse a la mesa si está libre y no está ya sobre
% la mesa en el tiempo T, es decir, si es que no está sobre la mesa actualmente.
movimientoposible(X,mesa,T) :- bloquelibre(X,T), not sobre(X,mesa,T).

% Esta línea indica que no puede haber un modelo en el cual en el tiempo límite
% los bloques no se encuentran en la configuración objetivo.
:- not objetivo(bound).

% ----------------------------------- Condiciones extras -----------------------------------%

% Esta condición establece que un deteminado bloque X no se puede mover a 2 lugares distintos al mismo tiempo.
:- ejecutar(X,Y,T), ejecutar(X,Z,T), tiempo(T), Y!=Z, X!=Y.

% Esta condición establece que si se quiere poner un bloque X sobre un bloque Y, no se puede poner el bloque Y sobre un bloque Z en un mismo tiempo.
:- ejecutar(X,Y,T), ejecutar(Y,Z,T), tiempo(T), X!=Z.

% Esta condición establece que no se pueden poner 2 bloques distintos sobre un mismo bloque en un mismo tiempo.
:- ejecutar(X,Y,T), ejecutar(Z,Y,T), tiempo(T), X!=Z.

% Esta condición establece que no se puede poner un bloque encima de otro y que al mismo tiempo el bloque que está debajo se ponga encima del otro bloque.
:- ejecutar(X,Y,T), ejecutar(Y,X,T), tiempo(T).

% ------------------------------------------------------------------------------------------%

bloque(b0). 

bloque(b1). 

bloque(b2). 

bloque(b3). 

bloque(b4). 

bloque(b5). 

bloque(b6). 

bloque(b7). 

bloque(b8). 

bloque(b9). 

bloque(b10). 

bloque(b11). 

bloque(b12). 

bloque(b13). 

bloque(b14). 

bloque(b15). 

bloque(b16). 

bloque(b17). 

bloque(b18). 

bloque(b19). 

 
 
 

sobre(b18,mesa,0). 

sobre(b5,b18,0). 

sobre(b11,b5,0). 

sobre(b3,b11,0). 

sobre(b17,mesa,0). 

sobre(b16,b17,0). 

sobre(b10,b16,0). 

sobre(b8,b10,0). 

sobre(b2,b8,0). 

sobre(b0,mesa,0). 

sobre(b12,b0,0). 

sobre(b1,b12,0). 

sobre(b15,mesa,0). 

sobre(b9,b15,0). 

sobre(b7,mesa,0). 

sobre(b4,b7,0). 

sobre(b13,b4,0). 

sobre(b6,b13,0). 

sobre(b19,b6,0). 

sobre(b14,b19,0). 

 
 
 

objetivo(T) :-  

    sobre(b7,mesa,T), 

    sobre(b2,mesa,T), 

    sobre(b4,b2,T), 

    sobre(b8,b4,T), 

    sobre(b6,mesa,T), 

    sobre(b5,mesa,T), 

    sobre(b19,mesa,T), 

    sobre(b15,b19,T), 

    sobre(b17,b15,T), 

    sobre(b10,b17,T). 
% #minimize {1 , C : ejecutar(X , C )}.

accion_en_t(T,A) :- ejecutar(X,Y,T), A = (X,Y).

#minimize {1, A : accion_en_t(T,A)}.

#show ejecutar/3.

