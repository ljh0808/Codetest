import java.util.*;
import java.lang.*;

class Solution {
    public double solution(int[] arr) {

        return Arrays.stream(arr).average().getAsDouble();
    }
}