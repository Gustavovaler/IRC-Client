package main
//algo para hacer
import (
	"bufio"
	"fmt"
	"net"
	"net/textproto"
	"strings"
)

func main() {
	protocol := "tcp"
	server := "irc.freenode.net:6667"

	//Inicio la conexion
	conn, err := net.Dial(protocol, server)
	if err != nil {
		panic(err)
	}
	// envio las credenciales

	fmt.Fprintf(conn, "USER %s 8 * :%s\r\n", "GustavoKirchbnet", "GustavoKirchbnet")
	fmt.Fprintf(conn, "NICK %s\r\n", "NestorKirchner")
	fmt.Fprintf(conn, "JOIN %s\r\n", "#gus-challenge")

	// Cpturamos la respuesta
	reader := bufio.NewReader(conn)
	// Formateamos a string
	tp := textproto.NewReader(reader)

	loading := false

	for loading == false {
		// Mostramos por pantalla
		line, err := tp.ReadLine()
		if err != nil {
			panic(err)
		}
		fmt.Println("%s\n", line)
		// Evaluamos el estado de la conexion
		if strings.Contains(line, "/NAMES list") {
			loading = true
		}

	}
	//enviamos mensaje

	fmt.Fprintf(conn, "PRIVMSG #gus-challenge  :Hola desde bot Go!\r\n")

}
