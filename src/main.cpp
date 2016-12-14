#include "settings.hpp"
#include <stdio.h>

int main(int argc, char** argv)
{
	if (argc == 1)
	{
		printf("Missing arguments.\nTry `bfgame --help` for help.");
		return -1;
	}
}