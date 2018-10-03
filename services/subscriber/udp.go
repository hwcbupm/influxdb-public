package subscriber

import (
	"net"

	"github.com/influxdata/influxdb/coordinator"
	"strconv"
	"github.com/influxdata/influxdb/models"
	"strings"
)

// UDP supports writing points over UDP using the line protocol.
type UDP struct {
	addr string
}

// NewUDP returns a new UDP listener with default options.
func NewUDP(addr string) *UDP {
	return &UDP{addr: addr}
}

// String returns the string representation of the point.
func OpenTSDBString(p *models.Point) string {
	nano := strconv.FormatInt((*p).UnixNano(), 10)
	it := (*p).FieldIterator()
	if it.Next() {
		value, err := it.FloatValue()
		if err != nil {
			return ""
			//panic(err)
		}
		return string((*p).Key()) + " " + nano[:len(nano)-6] + " " + strconv.FormatFloat(value,'f',3, 64)
	} else {
		//panic("unexpected data")
		return ""
	}
}

// WritePoints writes points over UDP transport.
func (u *UDP) WritePoints(p *coordinator.WritePointsRequest) (err error) {
	con, err := net.Dial("tcp", "127.0.0.1:4242")
	//con, err = net.DialUDP("udp", nil, addr)
	if err != nil {
		return
	}
	defer con.Close()

	source := strings.Split(u.addr, ":")[0]

	for _, pt := range p.Points {
		_, err = con.Write([]byte("put " + OpenTSDBString(&pt) + " source=" + source + "\n"))
		if err != nil {
			//panic("Failed to replicate")
			return
		}

	}
	return
}

