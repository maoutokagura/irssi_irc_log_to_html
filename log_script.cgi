#!/usr/bin/perl

$buffer = $ENV{'QUERY_STRING'};
($channel,$date,$enc) = split(/&/,$buffer);

$i;
@nick;
@colors = ('aqua','yellow','Teal','Purple','fuchsia','lime','orange','red','Maroon','Green');
$logdir = "/home/2TB/irclog/";
$script_name = "log_script.cgi";

print "Content-type: text/html", "\n\n";
print <<EOM;
<html>\n <head>\n
<link rel="stylesheet" type="text/css" href="../../irclog.css">\n
</head>\n <body>\n
EOM

if ($buffer ==  NULL){
    &getfol;
}elsif($date == NULL){
    &getfiles;
}else{
    &getlog;
}
print <<EOM;
</body>\n
</html>\n
EOM

sub getlog{
    chdir($logdir);
    my @follist= glob "*/";
    my $folname = $follist[$channel - 1];
    print "$folname<br>\n";
    chdir("$logdir$folname");
    open(IN, $date);
    while ( $line = <IN>) {
	print &rewrite($line);
	$i++;
    }
    print @nick;
    close(IN);
}

sub getfiles{
    my $req = $channel;
    chdir("$logdir");
    my @follist= glob "*/";
    my $folname = $follist[$req - 1];
    print "$folname<br>\n aa\n";
    chdir("$logdir$folname");
    my @filelist= glob "*.txt";
    foreach my $file (sort @filelist){
	next if( $file =~ /^\.{1,2}$/ );
	&href("$script_name?$channel&$file",$file,br);
    }
}

sub getfol{
    chdir("$logdir");
    my @file= glob "*/";
    my $i = 1;
    foreach my $direct (@file){
	next if( $file =~ /^\.{1,2}$/ );
	&href("$script_name?$i",$direct,br);
	$i = $i + 1;
    }
}

sub href {
    my($url, $alt, $br) = @_;
    print"<a href\=$url>$alt<\/a>";
    if ($br eq br) {print "<br>";}
    print "\n";
}

sub rewrite{
    my $tennpo = $_ = $string = @_[0];
    my $nick_color;

    if(s/^(\d\d:\d\d)\s\W(\S+?:).*/\2/){
	$tennpo = $_ . "<br>";
	if (!grep(/$tennpo/,@nick)){
	    push(@nick,$tennpo);
	}
    }
    $nick_color = @colors[(&nick_search($tennpo,@nick) % scalar(@colors))];
    $string =~ s/^(\d\d:\d\d)\s\W(\S+?:)/<span style="color:blue;">\1<\/span><span style="color:$nick_color ;"> \2<\/span>/;
    if ($string =~ m/.*(http.*?)\s/o){
	$tennpo = $1;
	$string =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<a href=\"$1\" target="_blank" >$1 <\/a>/gi;
	if($tennpo =~ /(jpg)|(png)|(gif)$/){
	    return "<img height=200 src=\"$tennpo \"><br>" . $string . "<br>\n";
	}
	if($tennpo =~ /http:\/\/www\.youtube\.com\/.*v=([^&]+).*/){
	    return "<img height=200 src=\"http\:\/\/i.ytimg\.com\/vi\/$1/default.jpg \"><br>" . $string . "<br>\n";
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
    my ($what, @area) = @_;
    foreach my $idx (0..$#area) {
	if ($area[$idx] =~ /$what/) { return $idx }
    }
    return -1;
}
