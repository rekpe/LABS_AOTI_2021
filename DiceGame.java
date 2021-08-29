import java.util.Random; 

public class RandomTester 
{
    public static int getRandomNumber(int seed) { 
	   Random randomGenerator; 
	   randomGenerator = new Random(); 
	   return randomGenerator.nextInt(seed) + 1; 
   } 
 
   public static void throwDice() { 
	    int index = 0; 
		do { 
			index = getRandomNumber(6);
			System.out.println(index);
		} 
		while (index != 6); 
   }
}