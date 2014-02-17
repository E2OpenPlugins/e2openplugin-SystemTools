#!/bin/sh
memtotal=`cat /proc/meminfo | grep "MemTotal:" | sed -e 's/MemTotal://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
memfree=`cat /proc/meminfo | grep "MemFree:" | sed -e 's/MemFree://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
buffers=`cat /proc/meminfo | grep "Buffers" | sed -e 's/Buffers://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
cached=`cat /proc/meminfo | grep -m 1 "Cached:" | sed -e 's/Cached://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
swapcached=`cat /proc/meminfo | grep "SwapCached:" | sed -e 's/SwapCached://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
swaptotal=`cat /proc/meminfo | grep "SwapTotal:" | sed -e 's/SwapTotal://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
swapfree=`cat /proc/meminfo | grep "SwapFree" | sed -e 's/SwapFree://g' | sed -e 's/\ kB//g' | sed -e 's/^[ \t]*//'`
memused=$(($memtotal - $memfree - $cached - $buffers))
swapused=$(($swaptotal - $swapfree))
avblmemory=$(($memfree + $buffers + $cached))
avblmemorywswap=$(($memfree + $buffers + $cached + $swapfree))
echo "Total memory:	$memtotal kB"
echo "Used memory:	$memused kB note: this is just the unusable mem"
echo "Free memory:	$memfree kB note: this just the unused mem"
echo "Buffers:    	$buffers kB"
echo "Cached :    	$cached kB"
echo ""
echo "Actual base memory still avbl to apllications: $avblmemory kb"
#echo "SwapCached :		$swapcached kB"
if [ "$swaptotal" -gt 0 ] ; then
echo ""
echo "SwapTotal:  	$swaptotal kB"
echo "Swapused:	$swapused kB"
echo "SwapFree:  	$swapfree kB"
echo ""
echo "Total memory(with swap) still avbl to applications: $avblmemorywswap kB"
fi

#end
