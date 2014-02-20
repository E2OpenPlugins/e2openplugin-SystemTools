#!/bin/sh
memtotal=`cat /proc/meminfo | grep "MemTotal:" | sed -e 's/MemTotal://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
memfree=`cat /proc/meminfo | grep "MemFree:" | sed -e 's/MemFree://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
buffers=`cat /proc/meminfo | grep "Buffers" | sed -e 's/Buffers://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
cached=`cat /proc/meminfo | grep -m 1 "Cached:" | sed -e 's/Cached://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
swapcached=`cat /proc/meminfo | grep "SwapCached:" | sed -e 's/SwapCached://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
swaptotal=`cat /proc/meminfo | grep "SwapTotal:" | sed -e 's/SwapTotal://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
swapfree=`cat /proc/meminfo | grep "SwapFree" | sed -e 's/SwapFree://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
meminuse=$(($memtotal - $memfree))
memused=$(($memtotal - $memfree - $cached - $buffers))
swapused=$(($swaptotal - $swapfree))
avblmemory=$(($memfree + $buffers + $cached))
avblmemorywswap=$(($memfree + $buffers + $cached + $swapfree))
echo "	Total	Used	Free"
echo ""
echo "mem: 	$memtotal kB	$meminuse kB	$memfree kB"
echo "-/+BufCaches		$memused kB	$avblmemory kB"
if [ "$swaptotal" -gt 0 ] ; then
echo "swap:	$swaptotal kB	$swapused kB	$swapfree kB"
echo ""
echo "The avbl memory for applications = $avblmemorywswap kB"
else
echo ""
echo "The avbl memory for applications = $avblmemory kB"
fi
echo ""

#end
