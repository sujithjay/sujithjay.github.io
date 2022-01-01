tags: #joins #query-processing
source: [[Skew-Strikes-Back]]

$$Q_∆ = R(A,B) ⋈  S(B,C) ⋈ T(A,C)$$

Traditional join plan for the triangle query given above, the simplest cyclic query, involves determining the best pair-wise join plan among three.

![[Pairwise.png]]

Let us take an example of a family of instances for which any of the above three join plans must run in time $$Ω(N^2)$$ because the intermediate relation P is too large.

![[InstanceFamily.png]]

In the above instance, each relation has N = 2m + 1 tuples and $$|Q_∆| = 3m+1$$; however, any pair-wise join has size $$ m^2 + m$$

Thus, any of the three join plans will take $$Ω(N^2)$$ time. This bound holds even if we allow projections.