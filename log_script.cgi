#!/usr/bin/perl

use strict;

my $buffer = $ENV{'QUERY_STRING'};
my ($channel,$date,$enc) = split(/&/,$buffer);

my $i;
my @nick;
my @colors = ('aqua','yellow','lime','fuchsia','orange','Teal','red','Purple','Maroon','Green');
my $logDir = "/home/2TB/irclog/";
my $script_name = "log_script.cgi";

print "Content-type: text/html", "\n\n";
print <<EOM;
<html>\n <head>\n
<link rel="stylesheet" type="text/css" href="../../irclog.css">\n
</head>\n <body>\n<div id="main">
EOM

chdir("$logDir");
my @follist= glob "*/";

if ($buffer ==  undef){
    &getfol;
}elsif($date == undef){
    &getfiles;
}else{
    &getlog;
}
print <<EOM;
</div>\n</body>\n</html>\n
EOM

sub getlog{
    my $folname = $follist[$channel - 1];
    print "$folname<br>\n";
    chdir("$logDir$folname");
    open(IN, $date);
#    my $line;
#    while ( $line = <IN>) {
#	print &rewrite($line);
#    }
    foreach my $line (<IN>){
	print &rewrite($line);
    }
    print @nick;
    close(IN);
}

sub getfiles{
    my $req = $channel;
    my $folname = $follist[$req - 1];
    print "$folname<br>\n aa\n";
    chdir("$logDir$folname");
    my @filelist= glob "*.txt";
    foreach my $file (sort @filelist){
	next if( $file =~ /^\.{1,2}$/ );
	&href("$script_name?$channel&$file",$file,"br");
    }
}

sub getfol{
    my $i = 1;
    foreach my $direct (@follist){
	next if( $direct =~ /^\.{1,2}$/ );
	&href("$script_name?$i",$direct,"br");
	$i = $i + 1;
    }
}

sub href {
    my($url, $alt, $br) = @_;
    print"<a href\=$url>$alt<\/a>";
    if ($br eq "br") {print "<br>";}
    print "\n";
}

sub rewrite{
    my $string = @_[0];
    my $tmp;
    my $nick_color;

    
    if($string =~ m/^(\d\d:\d\d)\s\W(\S+?:)/){
	$tmp = $2 . "<br>";
	if (!grep(/$tmp/,@nick)){
	    push(@nick,$tmp);
	}
    }
    $nick_color = @colors[(&nick_search($tmp,@nick) % scalar(@colors))];
    $string =~ s/</\&lt\;/g;
    $string =~ s/^(\d\d:\d\d)\s\W(\S+?:)/<span style="color:blue;">\1<\/span><span style="color:$nick_color ;"> \2<\/span>/;
    if ($string =~ m/.*(http.*?)\s/o){
	$tmp = $1;
	$string =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href=\"$1\" target="_blank" >$1 <\/a>/gi;
	if($tmp =~ /(jpg)|(png)|(gif)$/){
	    return "<img height=200 src=\"$tmp \"><br>" . $string . "<br>\n";
	}elsif($tmp =~ /http:\/\/www\.youtube\.com\/.*v=([^&]+).*/){
	    return "<img height=200 src=\"http\:\/\/i.ytimg\.com\/vi\/$1/default.jpg \"><br>" . $string . "<br>\n";
	}elsif($tmp =~ /http:\/\/www\.nicovideo\.jp\/watch\/.*sm([^&]+).*/){
	    return "<img height=200 src=http://tn-skr2.smilevideo.jp/smile?i=$1 \"><br>" . $string . "<br>\n";
	}elsif($tmp =~ /http:\/\/shindanmaker.com\/([^&]+).*/){
	    return $string ."<br>\n";
	}else{
	    return "<img src=\"http\:\/\/capture.heartrails.com\/\?$tmp \"><br>" . $string . "<br>\n";
	}
	return $string ."<br>\n";
    }else{
	return $string . "<br>\n";
    }
}

sub rewrite_time{
    my $time =@_;
}

sub nick_search {
    my $area;
    my ($what, @area) = @_;
    foreach my $idx (0..$#area) {
	if ($area[$idx] =~ /$what/) { return $idx }
    }
    return -1;
}
