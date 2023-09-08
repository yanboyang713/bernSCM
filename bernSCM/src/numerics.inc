c     derived parameters for numerical solution


c     propagator structures
      TYPE :: Prop              !propagators
      sequence
      integer  :: nscale
      real*8   :: propm(nscalemax+1)
      real*8   :: propf(nscalemax+1)
      real*8   :: propfo(nscalemax+1)
      real*8   :: x
      END TYPE Prop

      type(Prop) :: L
      type(Prop) :: O

      common /prop/ L,O
      
